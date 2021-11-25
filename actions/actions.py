from datetime import datetime 

from typing import Any, Text, Dict, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType, FollowupAction, AllSlotsReset
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

#tasks = "->"
tasks = []
ask_gad = False
ask_k10 = True


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
            dispatcher.utter_message(response="utter_nice_name", name=name)
        
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

        mood = tracker.slots.get("mood")
        if mood in ["Excited","Happy","Calm","Content","Loved","Maybe later", "Not sure"]:
            slots_mapped_in_domain.remove("mood_intense")
            slots_mapped_in_domain.remove("mood_reason")
            slots_mapped_in_domain.remove("self_harm")
        
        mi = tracker.slots.get("mood_intense")
        if mi in ["Moderate","Low", None]:
            slots_mapped_in_domain.remove("self_harm")
            slots_mapped_in_domain.remove("if_helpful")

        return slots_mapped_in_domain
    
        
    def validate_mood(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        global ask_gad
        mood = tracker.slots.get("mood")
        if mood in ["Maybe later", "Not sure"]:
            dispatcher.utter_message(text=f"No problem. 🙂")
        if mood in ["Excited","Happy","Calm","Content","Loved"]:
            dispatcher.utter_message(text=f"👍 Great!")
        if mood in ["Anxious"]:
            print("flag for GAD")
            ask_gad = True
        else:
            dispatcher.utter_message(text=f"It can be difficult to identify our feelings, thank you for being aware.")
        
        return {"mood":mood}


    def validate_self_harm(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        sh = tracker.slots.get("self_harm")
        if sh in ["/affirm"]:
            dispatcher.utter_message(text=f"Please use the following services for help")
            dispatcher.utter_message(text=f"iCALL: a psychological helpline that aims to provide high quality telephone counselling.\n \n022-25521111\n \n+91-9152987821\n \nhttps://icallhelpline.org/")
            dispatcher.utter_message(text=f"AASRA: Whatever your concerns are, you can be rest assured that you will receive non-judgmental and non-critical listening.\n \n+91-9820466726\n \nhttp://www.aasra.info/")
        
            #dispatcher.utter_message(text=f"iCALL: a psychological helpline that aims to provide high quality telephone counselling.<br>022-25521111<br>+91-9152987821<br>https://icallhelpline.org/")
            #dispatcher.utter_message(text=f"AASRA: Whatever your concerns are, you can be rest assured that you will receive non-judgmental and non-critical listening.<br>+91-9820466726<br>http://www.aasra.info/")
        
        return {"self_harm":sh}

        
# class ActionSubmitK10Results(Action):
#     def name(self) -> Text:
#         return "action_submit_k10"
#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],) -> List[Dict]:

#         name = tracker.get_slot("name")
#         age = tracker.get_slot("age")
#         feel = tracker.get_slot("feel")
#         q01,q02,q03,q04,q05,q06,q07,q08,q09,q10 = tracker.get_slot("q01"),tracker.get_slot("q02"),tracker.get_slot("q03"),tracker.get_slot("q04"),tracker.get_slot("q05"),tracker.get_slot("q06"),tracker.get_slot("q07"),tracker.get_slot("q08"),tracker.get_slot("q09"),tracker.get_slot("q10")
#         score = int(q01)+int(q02)+int(q03)+int(q04)+int(q05)+int(q06)+int(q07)+int(q08)+int(q09)+int(q10)
#         now = datetime.now()
#         #timestamp = datetime.timestamp(now)
        
#         # Save as txt for each user
#         # form_results = str(name)+"\n"+str(age)+"\n"+str(feel)+"\n"+str(q01)+"\n"+str(q02)+"\n"+str(q03)+"\n"+str(q04)+"\n"+str(q05)+"\n"+str(q06)+"\n"+str(q07)+"\n"+str(q08)+"\n"+str(q09)+"\n"+str(q10)+"\n"+str(score)+"\n"+str(result)
#         # f = open(name+"_k10_results.txt", "a")
#         # f.write(form_results)
#         # f.close()

#         # Save as csv for all users
#         form_results = str(name)+","+str(age)+","+str(feel)+","+str(q01)+","+str(q02)+","+str(q03)+","+str(q04)+","+str(q05)+","+str(q06)+","+str(q07)+","+str(q08)+","+str(q09)+","+str(q10)+","+str(score)+","+str(now)+"\n"
#         f = open("k10_results.csv", "a")
#         f.write(form_results)
#         f.close()

#         result = "Your K10 Test Score is: " + str(score) + "/50" + "\n"
#         if score >= 10 and score <= 19:
#             result = result + "You are likely to be well.\n"
#         if score >= 20 and score <= 24:
#             result = result + "You are likely to have a mild mental disorder.\n"
#         if score >= 25 and score <= 29:
#             result = result + "You are likely to have moderate mental disorder.\n"
#         if score >= 30 and score <= 50:
#             # additional text for severe
#             result = result + "You are likely to have a severe mental disorder.\n" #color

#         dispatcher.utter_message(text = "Thanks "+name+", your answers have been recorded!")
#         dispatcher.utter_message(text = result)
#         dispatcher.utter_message(text = "If you wish to know more about the K10 Test, follow the link: https://www.tac.vic.gov.au/files-to-move/media/upload/k10_english.pdf")
#         return []



class ValidatePlandayForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_planday_form"

    
    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:
        
        plan_day = tracker.slots.get("plan_day")
        if plan_day in ["/deny"]:
            print("skipped day planner")
            slots_mapped_in_domain.remove("task")
            slots_mapped_in_domain.remove("more_task")
            
        
        return slots_mapped_in_domain

    
    
    def validate_plan_day(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        plan_day = tracker.slots.get("plan_day")
        if plan_day in ["/affirm"]:
            print("start loop for tasks")
            dispatcher.utter_message(text = "Great, Let me know what's your plan for today?")
            return {"task": None, "more_task": None}
        else:
            dispatcher.utter_message(response="utter_happy")
        
        return {"plan_day": plan_day}
        
    
    def validate_task(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        global tasks
        task = tracker.slots.get("task")
        if task is not None:
            #tasks = tasks + task + "\n" + "->"
            tasks.append(task)
            
            msg = "Tasks for today:\n✔️"+'\n✔️'.join(str(p) for p in tasks)
            print(msg)
            dispatcher.utter_message(text = msg)
            #dispatcher.utter_message(text = f"Tasks for today: <br>✔️"+' <br>✔️'.join(str(p) for p in tasks))
            
        return {"task": task}
    
    
    
    def validate_more_task(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        more_task = tracker.slots.get("more_task")
        name = tracker.slots.get("name")

        if more_task in ["/deny"]:
            dispatcher.utter_message(text = f"Tasks for today:\n✔️"+'\n✔️'.join(str(p) for p in tasks))
            #dispatcher.utter_message(text = f"Tasks for today:<br>✔️"+'<br>✔️'.join(str(p) for p in tasks))
            dispatcher.utter_message(response="utter_happy")
            #dispatcher.utter_message(response="utter_ask_more_task")
            
            now = datetime.now()
            #print(name,tasks,now)
            t = str(name or 'guest') +','+ ','.join(tasks) +','+ str(now) + '\n'
            print("saving: " + t)

            f = open("planner.txt", "a")
            f.write(t)
            f.close()

            return {"more_task": more_task}
        
        if more_task in ["/affirm"]:
            return {"task": None, "more_task": None}
        




class ValidateK10Form(FormValidationAction):
    def name(self) -> Text:
        return "validate_k10_form"

    
    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:
        
        if ask_k10 is False:
            print("skipped K10")
            slots = ["take_k10", "q01", "q02", "q03", "q04", "q05", "q06", "q07", "q08", "q09", "q10"]
            for slot in slots:
                slots_mapped_in_domain.remove(slot)
        
        else:
            print("K10")
            take_k10 = tracker.slots.get("take_k10")
            if take_k10 in ["/deny"]:
                print("deny K10")
                slots = ["q01", "q02", "q03", "q04", "q05", "q06", "q07", "q08", "q09", "q10"]
                for slot in slots:
                    slots_mapped_in_domain.remove(slot)

        return slots_mapped_in_domain


    def validate_take_k10(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        take_k10 = tracker.slots.get("take_k10")
        
        if take_k10 in ["/affirm"]:
            print("started K10")
            dispatcher.utter_message(text = f"K10 Test:")
            
            
        return {"take_k10":take_k10} 

    def validate_q10(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        name = tracker.get_slot("name")
        age = tracker.get_slot("age")
        feel = tracker.get_slot("feel")
        q01,q02,q03,q04,q05,q06,q07,q08,q09,q10 = tracker.get_slot("q01"),tracker.get_slot("q02"),tracker.get_slot("q03"),tracker.get_slot("q04"),tracker.get_slot("q05"),tracker.get_slot("q06"),tracker.get_slot("q07"),tracker.get_slot("q08"),tracker.get_slot("q09"),tracker.get_slot("q10")
        score = int(q01)+int(q02)+int(q03)+int(q04)+int(q05)+int(q06)+int(q07)+int(q08)+int(q09)+int(q10)
        now = datetime.now()
        

        # Save as csv for all users
        form_results = str(name)+","+str(age)+","+str(feel)+","+str(q01)+","+str(q02)+","+str(q03)+","+str(q04)+","+str(q05)+","+str(q06)+","+str(q07)+","+str(q08)+","+str(q09)+","+str(q10)+","+str(score)+","+str(now)+"\n"
        f = open("k10_results.csv", "a")
        f.write(form_results)
        f.close()

        result = "Your K10 Test Score is: " + str(score) + "/50" + "\n \n"
        if score >= 10 and score <= 19:
            result = result + "You are likely to be well.\n \n "
        if score >= 20 and score <= 24:
            result = result + "You are likely to have a mild mental disorder.\n \n"
        if score >= 25 and score <= 29:
            result = result + "You are likely to have moderate mental disorder.\n \n"
        if score >= 30 and score <= 50:
            # additional text for severe
            result = result + "You are likely to have a severe mental disorder.\n \n" #color

        dispatcher.utter_message(text = "Thanks "+str(name or 'guest')+", your answers have been recorded!")
        dispatcher.utter_message(text = result)
        dispatcher.utter_message(text = "If you wish to know more about the K10 Test, follow the link: https://www.tac.vic.gov.au/files-to-move/media/upload/k10_english.pdf")
        
        return {"q10":score}




class ValidateGadForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_gad_form"

    
    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:
        mood = tracker.slots.get("mood")
        if mood not in ["Anxious"] and ask_gad == False:
            print("skipped GAD7")
            slots = ["take_gad", "gq1", "gq2", "gq3", "gq4", "gq5", "gq6", "gq7"]
            for slot in slots:
                slots_mapped_in_domain.remove(slot)
        
        else:
            print("GAD7")
            take_gad = tracker.slots.get("take_gad")
            if take_gad in ["/deny"]:
                print("deny GAD7")
                slots = ["gq1", "gq2", "gq3", "gq4", "gq5", "gq6", "gq7"]
                for slot in slots:
                    slots_mapped_in_domain.remove(slot)

        return slots_mapped_in_domain


    def validate_take_gad(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        take_gad = tracker.slots.get("take_gad")
        
        if take_gad in ["/affirm"]:
            print("started GAD7")
            dispatcher.utter_message(text = f"Over the last 2 weeks, how often have you been bothered by any of the following problems?")
            
            
        return {"take_gad":take_gad} 

    def validate_gq7(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        name = tracker.slots.get("name")
        take_gad = tracker.slots.get("take_gad")
        gq1,gq2,gq3,gq4,gq5,gq6,gq7 = tracker.get_slot("gq1"),tracker.get_slot("gq2"),tracker.get_slot("gq3"),tracker.get_slot("gq4"),tracker.get_slot("gq5"),tracker.get_slot("gq6"),tracker.get_slot("gq7")
        score = int(gq1)+int(gq2)+int(gq3)+int(gq4)+int(gq5)+int(gq6)+int(gq7)
        print(score,"/21")

        result = "Your Generalised Anxiety Disorder Questionnaire \n \n (GAD-7) Total is: " + str(score) + "/21" + "\n \n"
        if score >= 0 and score <= 4:
            result = result + "You are likely to be well. \n \n"
        if score >= 5 and score <= 9:
            result = result + "You are likely to have a mild anxiety. \n \n"
        if score >= 10 and score <= 14:
            # further evaluation is recommended when the score is 10 or greater
            # additional text for severe
            result = result + "You are likely to have moderate anxiety. \n \n"
        if score >= 15 and score <= 21:
            # further evaluation is recommended when the score is 10 or greater
            # additional text for severe
            result = result + "You are likely to have a severe mental anxiety. \n \n" #color

        dispatcher.utter_message(text = "Thanks "+str(name or 'guest')+", your answers have been recorded!")
        dispatcher.utter_message(text = result)
        dispatcher.utter_message(text = "If you wish to know more about the GAD-7 Test, follow the link: https://patient.info/doctor/generalised-anxiety-disorder-assessment-gad-7#ref-2")

        # Save as csv for all users
        now = datetime.now()
        form_results = str(name)+","+str(gq1)+","+str(gq2)+","+str(gq3)+","+str(gq4)+","+str(gq5)+","+str(gq6)+","+str(gq7)+","+str(score)+","+str(now)+"\n"
        f = open("gad7_results.csv", "a")
        f.write(form_results)
        f.close()

        return {"gq7":score}




class ActionCarousel(Action):
    def name(self) -> Text:
        return "action_carousel"
    
    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Core Exercises",
                        "subtitle": "Choose an activity",
                        "image_url": "C:/Users/Admin/SilentMoon/Forms/ui/img/core.jpg",
                        "buttons": [ 
                            {
                            "title": "Daily check",
                            "payload": "main_form",
                            "type": "postback"
                            },
                            {
                            "title": "Mood Booster",
                            "payload": "mood_booster",
                            "type": "postback"
                            },
                            {
                            "title": "Journal entries",
                            "payload": "journal_entries",
                            "type": "postback"
                            },
                            {
                            "title": "To-do list",
                            "payload": "tasks",
                            "type": "postback"
                            },
                            {
                            "title": "Thought of the day",
                            "payload": "totd",
                            "type": "postback"
                            },
                        ]
                    },
                    {
                        "title": "Meditation & Mindfulness",
                        "subtitle": "Read, listen, follow",
                        "image_url": "C:/Users/Admin/SilentMoon/Forms/ui/img/meditation.jpg",
                        "buttons": [ 
                            {
                            "title": "Basic Meditation",
                            "payload": "Basic Meditation",
                            "type": "postback"
                            },
                            {
                            "title": "Calming Meditation ",
                            "payload": "Calming Meditation ",
                            "type": "postback"
                            },
                            {
                            "title": "Basic Stillness",
                            "payload": "Basic Stillness",
                            "type": "postback"
                            }
                        ]
                    },
                    {
                        "title": "Calm down",
                        "subtitle": "Watch, listen, relax",
                        "image_url": "C:/Users/Admin/SilentMoon/Forms/ui/img/calm.jpg",
                        "buttons": [ 
                            {
                            "title": "Calming Breaths ",
                            "payload": "Calming Breaths ",
                            "type": "postback"
                            },
                            {
                            "title": "Releasing Tension ",
                            "payload": "Releasing Tension ",
                            "type": "postback"
                            },
                            {
                            "title": "Calming Visualisation ",
                            "url": "C:/Users/Admin/SilentMoon/Forms/ui/img/calm.jpg",
                            "type": "web_url"
                            }
                        ]
                    },
                    {
                        "title": "Screening tools",
                        "subtitle": "Easy-to-use, self-administered patient questionnaires",
                        "image_url": "C:/Users/Admin/SilentMoon/Forms/ui/img/screeningtools.jpg",
                        "buttons": [ 
                            {
                            "title": "K10 Test",
                            "payload": "/k10_form",
                            "type": "postback"
                            },
                            {
                            "title": "GAD-7 Test",
                            "payload": "/gad_form ",
                            "type": "postback"
                            }
                        ]
                    }
                ]
                }
        }
        dispatcher.utter_message(attachment=message)
        return []



class ActionResetAllSlots(Action):

    def name(self) -> Text:
        return "action_reset_all_slots"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        global tasks, ask_gad, ask_k10
        tasks = []
        ask_gad = False
        ask_k10 = True
        return [AllSlotsReset()]



class ActionResetPlanday(Action):

    def name(self) -> Text:
        return "action_reset_planday"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        #
        return [SlotSet("task", None), SlotSet("more_task", None), SlotSet("plan_day", None)]


class ActionResetMain(Action):

    def name(self) -> Text:
        return "action_reset_main"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        #
        return [SlotSet("sleep_hours", None), SlotSet("blood_test", None), SlotSet("mood", None), SlotSet("mood_intense", None), SlotSet("mood_reason", None), SlotSet("self_harm", None)]


class ActionResetInit(Action):

    def name(self) -> Text:
        return "action_reset_init"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        #
        return [SlotSet("name", None), SlotSet("name_bot", None), SlotSet("bot_name", None), SlotSet("age", None)]


class ActionResetK10(Action):

    def name(self) -> Text:
        return "action_reset_k10"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        #
        return [SlotSet("take_k10", None), SlotSet("q01", None), SlotSet("q02", None), SlotSet("q03", None), SlotSet("q04", None), SlotSet("q05", None), SlotSet("q06", None), SlotSet("q07", None), SlotSet("q08", None), SlotSet("q09", None), SlotSet("q10", None)]


class ActionResetGAD(Action):

    def name(self) -> Text:
        return "action_reset_gad"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        global ask_gad
        #
        ask_gad = True
        return [SlotSet("take_gad", None), SlotSet("gq1", None), SlotSet("gq2", None), SlotSet("gq3", None), SlotSet("gq4", None), SlotSet("gq5", None), SlotSet("gq6", None), SlotSet("gq7", None)]

