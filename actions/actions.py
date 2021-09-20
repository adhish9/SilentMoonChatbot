from datetime import datetime 

from typing import Any, Text, Dict, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import (
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
    UserUtteranceReverted,
)
class ValidateInitForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_init_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:
        
        name_bot = tracker.slots.get("name_bot")
        if name_bot in ["/deny"]:
            slots_mapped_in_domain.remove("bot_name")

        return slots_mapped_in_domain

    def validate_name(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        name = tracker.slots.get("name")
        if name is not None:
            dispatcher.utter_message(response="utter_nice_name")
        
        return {"name":name}
    
    def validate_bot_name(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        bot_name = tracker.slots.get("bot_name")
        if bot_name is not None:
            dispatcher.utter_message(response="utter_thank_name")
        
        return {"bot_name":bot_name}

class ValidateMainForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_main_form"
    
    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:
        
        #name = tracker.slots.get("name")

        mood = tracker.slots.get("mood")
        if mood in ["Excited","Happy","Calm","Content","Loved"]:
            slots_mapped_in_domain.remove("mood_intense")
            slots_mapped_in_domain.remove("mood_reason")
            slots_mapped_in_domain.remove("self_harm")
        
        return slots_mapped_in_domain
    
        
    
    def validate_mood(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        mood = tracker.slots.get("mood")
        if mood in ["Maybe later"]:
            dispatcher.utter_message(text=f"Sure, no problem. 🙂")
        if mood in ["Excited","Happy","Calm","Content","Loved"]:
            dispatcher.utter_message(text=f"👍 Great!")
        else:
            dispatcher.utter_message(text=f"It can be difficult to identify our feelings, thank you for being aware.")
        
        return {"mood":mood}
        
class ActionSubmitK10Results(Action):
    def name(self) -> Text:
        return "action_submit_k10"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],) -> List[Dict]:

        name = tracker.get_slot("name")
        age = tracker.get_slot("age")
        feel = tracker.get_slot("feel")
        q01,q02,q03,q04,q05,q06,q07,q08,q09,q10 = tracker.get_slot("q01"),tracker.get_slot("q02"),tracker.get_slot("q03"),tracker.get_slot("q04"),tracker.get_slot("q05"),tracker.get_slot("q06"),tracker.get_slot("q07"),tracker.get_slot("q08"),tracker.get_slot("q09"),tracker.get_slot("q10")
        score = int(q01)+int(q02)+int(q03)+int(q04)+int(q05)+int(q06)+int(q07)+int(q08)+int(q09)+int(q10)
        now = datetime.now()
        #timestamp = datetime.timestamp(now)
        
        # Save as txt for each user
        # form_results = str(name)+"\n"+str(age)+"\n"+str(feel)+"\n"+str(q01)+"\n"+str(q02)+"\n"+str(q03)+"\n"+str(q04)+"\n"+str(q05)+"\n"+str(q06)+"\n"+str(q07)+"\n"+str(q08)+"\n"+str(q09)+"\n"+str(q10)+"\n"+str(score)+"\n"+str(result)
        # f = open(name+"_k10_results.txt", "a")
        # f.write(form_results)
        # f.close()

        # Save as csv for all users
        form_results = str(name)+","+str(age)+","+str(feel)+","+str(q01)+","+str(q02)+","+str(q03)+","+str(q04)+","+str(q05)+","+str(q06)+","+str(q07)+","+str(q08)+","+str(q09)+","+str(q10)+","+str(score)+","+str(now)+"\n"
        f = open("k10_results.csv", "a")
        f.write(form_results)
        f.close()

        result = "Your K10 Test Score is: " + str(score) + "\n"
        if score >= 10 and score <= 15:
            result = result + "You are likely to be well.\n"
        if score >= 16 and score <= 21:
            result = result + "You are likely to have a mild mental disorder.\n"
        if score >= 22 and score <= 29:
            result = result + "You are likely to have moderate mental disorder.\n"
        if score >= 30 and score <= 50:
            # additional text for severe
            result = result + "You are likely to have a severe mental disorder.\n" #color

        dispatcher.utter_message("Thanks "+name+", your answers have been recorded!")
        dispatcher.utter_message(result)
        return []