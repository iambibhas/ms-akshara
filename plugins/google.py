import datetime
import requests
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template


class GooglePlugin(WillPlugin):

    @respond_to("^google (?P<query>.*)")
    def hello(self, message, query=None):
        if query is None:
            self.say("search for what?", message=message)
        else:
            response = requests.get('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&safe=off&q={query}'.format(query=query))
            if response.status_code != 200:
                self.say("Couldn't fetch results: {}".format(response.reason))
            else:
                resp_json = response.json()
                if resp_json['responseStatus'] != 200:
                    self.say("Couldn't fetch results: {}".format(resp_json['responseDetails']))
                else:
                    context = {'results': resp_json.get('responseData').get('results')}
                    self.say(rendered_template("google_results.html", context), message=message, html=True)


