# -*- coding: utf-8 -*-
import logging
from .BaseHandlers import BaseHandler
from libs.SecurityDecorators import authenticated, game_started
from models.InformationTrade import InformationTrade
from models.Box import Box
from models.Team import Team
from tornado.options import options

class SocialMarketHandler(BaseHandler):

    @authenticated
    @game_started
    def get(self, *args, **kwargs):
        """ View the social information market """
        user = self.get_current_user()
        trades = InformationTrade.all()
        # Filter trades: don't show your own team's trades in the 'to buy' list
        # and maybe only show trades for boxes the team hasn't fully completed yet
        available_trades = [t for t in trades if t.seller_team_id != user.team.id]
        self.render("market/social.html", user=user, trades=available_trades, errors=None)

    @authenticated
    @game_started
    def post(self, *args, **kwargs):
        """ Buy an information trade """
        uuid = self.get_argument("uuid", "")
        trade = InformationTrade.by_uuid(uuid)
        user = self.get_current_user()
        team = user.team

        if trade and trade.seller_team_id != team.id:
            if team in trade.buyers:
                self.render("market/social.html", user=user, trades=InformationTrade.all(), errors=["Vous possédez déjà cette information."])
            elif team.money < trade.price:
                self.render("market/social.html", user=user, trades=InformationTrade.all(), errors=["Fonds insuffisants (Cauris)."])
            else:
                # Execute transaction
                team.money -= trade.price
                trade.seller_team.money += trade.price # Zuckerberg logic: peer-to-peer!
                trade.buyers.append(team)
                self.dbsession.add(team)
                self.dbsession.add(trade.seller_team)
                self.dbsession.add(trade)
                self.dbsession.commit()
                self.event_manager.push_score_update()
                self.redirect("/user/market/social")
        else:
            self.redirect("/user/market/social")

class CreateInformationTradeHandler(BaseHandler):

    @authenticated
    @game_started
    def post(self, *args, **kwargs):
        """ Create a new information trade (Sell info) """
        user = self.get_current_user()
        box_uuid = self.get_argument("box_uuid", "")
        title = self.get_argument("title", "")
        content = self.get_argument("content", "")
        price = int(self.get_argument("price", 100))

        box = Box.by_uuid(box_uuid)
        if box and title and content:
            trade = InformationTrade(
                seller_team_id=user.team.id,
                box_id=box.id,
                title=title,
                content=content,
                price=price
            )
            self.dbsession.add(trade)
            self.dbsession.commit()
            self.redirect("/user/missions") # Redirect to missions to see the confirmation
        else:
            self.redirect("/user/missions")
