from datetime import datetime 

from typing import Any, Text, Dict, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


from rasa_sdk.forms import FormValidationAction
#from rasa_sdk.events import SlotSet, EventType, FollowupAction, AllSlotsReset
from rasa_sdk.events import (
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
    UserUtteranceReverted,
    AllSlotsReset,
)

#email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#quotes
import requests



#tasks = "->"
#tasks = []
#ask_gad = False
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
    
    def validate_name_bot(
        
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        name_bot = tracker.slots.get("name_bot")
        if name_bot in ["/deny"]:
            dispatcher.utter_message(text=f"I'm excited to get to know you! Let's get started.")
        
        return {"name_bot":name_bot}
    

    def validate_bot_name(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        bot_name = tracker.slots.get("bot_name")
        name_bot = tracker.slots.get("name_bot")
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
            slots_mapped_in_domain.remove("if_helpful")
        
        mi = tracker.slots.get("mood_intense")
        if mi in ["Moderate","Low"]:
            slots_mapped_in_domain.remove("self_harm")
            slots_mapped_in_domain.remove("if_helpful")

        sh = tracker.slots.get("self_harm")
        if sh in ["/deny"]:
            slots_mapped_in_domain.remove("if_helpful")

        
        return slots_mapped_in_domain
    
    def validate_sleep_hours(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        sleep_hours = tracker.slots.get("sleep_hours")
        if sleep_hours in ["<5"]:
            dispatcher.utter_message(text=f"Sleep and mental health are closely connected. Sleep deprivation affects your psychological state and mental health.\n And those with mental health problems are more likely to have insomnia or other sleep disorders. Please make sure you get to bed early. ")
        elif sleep_hours in ["5-8", "8-10"]:
            dispatcher.utter_message(text=f"Sleeping helps us to recover from mental as well as physical exertion. \nSleep and health are strongly related - poor sleep can increase the risk of having poor health, and poor health can make it harder to sleep. Sleep disturbances can be one of the first signs of distress.")
        else:
            dispatcher.utter_message(text=f"While sleep requirements vary slightly from person to person, most healthy adults need 7 to 9 hours of sleep per night to function at their best.")

    def validate_mood(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        #global ask_gad
        mood = tracker.slots.get("mood")
        if mood in ["Maybe later", "Not sure"]:
            dispatcher.utter_message(text=f"No problem. 🙂")
            dispatcher.utter_message(text=f"It can be difficult to identify our feelings, thank you for being aware.")
        elif mood in ["Excited","Happy","Calm","Content","Loved"]:
            dispatcher.utter_message(text=f"👍 Great!")
        elif mood in ["Anxious"]:
            print("flag for GAD")
            #ask_gad = True
            dispatcher.utter_message(text=f"It can be difficult to identify our feelings, thank you for being aware.")
        else:
            dispatcher.utter_message(text=f"It can be difficult to identify our feelings, thank you for being aware.")
        
        return {"mood":mood}

    def validate_mood_reason(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        mood_reason = tracker.slots.get("mood_reason")
        if mood_reason in ["Work"]:
            dispatcher.utter_message(text=f"Sometimes, work can be major stressor in many people's lives. \nIt is important to find the right balance to stay focused and motivated.")
        elif mood_reason in ["Relationships"]:
            dispatcher.utter_message(text=f"Sometimes, personal relationships can be taxing and can even take a toll mentally. \nIt is important to be empathetic and compassionate towards other people in challenging situations.")
        elif mood_reason in ["Family related reasons"]:
            dispatcher.utter_message(text=f"Sometimes, personal relationships can be taxing and can even take a toll mentally. \nIt is important to be empathetic and compassionate towards other people in challenging situations.")
        elif mood_reason in ["Don't know"]:
            dispatcher.utter_message(text=f"It is okay to not know why you may be experiencing certain emotions. Let us help you figure them out.")
        
        return {"mood_reason":mood_reason}
            

    def validate_self_harm(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        sh = tracker.slots.get("self_harm")
        if sh in ["/affirm"]:
            dispatcher.utter_message(text=f"In case of self-harm or suicidal thoughts, it is necessary to seek professional help.")
            dispatcher.utter_message(text=f"Please use the following services for immediate assistance:")
            dispatcher.utter_message(text=f"iCALL: a psychological helpline that aims to provide high quality telephone counselling.\n022-25521111\n+91-9152987821\nhttps://icallhelpline.org/")
            dispatcher.utter_message(text=f"AASRA: Whatever your concerns are, you can be rest assured that you will receive non-judgmental and non-critical listening.\n+91-9820466726\nhttp://www.aasra.info/")
            #dispatcher.utter_message(text=f"iCALL: a psychological helpline that aims to provide high quality telephone counselling.<br>022-25521111<br>+91-9152987821<br>https://icallhelpline.org/")
            #dispatcher.utter_message(text=f"AASRA: Whatever your concerns are, you can be rest assured that you will receive non-judgmental and non-critical listening.<br>+91-9820466726<br>http://www.aasra.info/")
        else:
            dispatcher.utter_message(text=f"Okay, Great!")

        return {"self_harm":sh}
    

    def validate_if_helpful(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if_helpful = tracker.slots.get("if_helpful")
        if if_helpful in ["/affirm"]:
            dispatcher.utter_message(text=f"Alright, good.")
        
        if if_helpful in ["/deny"]:
            dispatcher.utter_message(text=f"Alright. Let’s work on it together.")
            
        return {"if_helpful":if_helpful}

        


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
        tasks = tracker.slots.get("tasks")
        if plan_day in ["/affirm"]:
            print("start loop for tasks")
            dispatcher.utter_message(text=f"Great, let me know what's your plan for today?")
            if tasks is not None: 
                tasks = tasks.split(",")
                dispatcher.utter_message(text = f"Tasks for today:\n✔️"+'\n✔️'.join(str(t) for t in tasks))
            return {"task": None, "more_task": None}
        else:
            dispatcher.utter_message(text=f"Alright. You can come back and plan your day by saying 'tasks', 'planner' or selecting 'To-do list' on the menu.")
        #    dispatcher.utter_message(text=f"Okay. Use the following menu to choose an activity.")
        
        return {"plan_day": plan_day}
        
    
    def validate_task(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        task = tracker.slots.get("task")
        tasks = tracker.slots.get("tasks")
        if tasks is None:
            tasks = []
        else:
            tasks = tasks.split(",")
        if task is not None:
            #tasks = tasks + task + "\n" + "->"
            tasks.append(task)
            
            msg = "Tasks for today:\n✔️"+'\n✔️'.join(str(t) for t in tasks)
            print(msg)
            dispatcher.utter_message(text = msg)
            #dispatcher.utter_message(text = f"Tasks for today: <br>✔️"+' <br>✔️'.join(str(p) for p in tasks))

        tasks = ",".join(tasks)
            
        return {"task":task, "tasks":tasks}
    
    
    
    def validate_more_task(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        more_task = tracker.slots.get("more_task")
        name = tracker.slots.get("name")
        tasks = tracker.slots.get("tasks")
        tasks = tasks.split(",")
        if more_task in ["/deny"]:
            dispatcher.utter_message(text = f"Tasks for today:\n✔️"+'\n✔️'.join(str(t) for t in tasks))
            #dispatcher.utter_message(text=f"Great. You can come back to this list by saying 'tasks', 'planner' or selecting 'To-do list' on the menu.")
            #dispatcher.utter_message(text=f"Great. Use the following menu to choose an activity.")
            #dispatcher.utter_message(text = f"Tasks for today:<br>✔️"+'<br>✔️'.join(str(p) for p in tasks))
            #dispatcher.utter_message(response="utter_happy")
            #dispatcher.utter_message(response="utter_ask_more_task")
            
            conversation_id=tracker.sender_id
            now = datetime.now()
            #print(name,tasks,now)
            t =  str(conversation_id)+','+str(name or 'guest')+','+','.join(tasks)+','+ str(now)+'\n'
            print("saving: " + t)

            f = open("store/planner.txt", "a")
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
            slots = ["take_k10", "q01", "q02", "q03", "q04", "q05", "q06", "q07", "q08", "q09", "q10", "email_result_k10", "email"]
            for slot in slots:
                slots_mapped_in_domain.remove(slot)
        
        else:
            print("K10")
            take_k10 = tracker.slots.get("take_k10")
            if take_k10 in ["/deny"]:
                print("deny K10")
                slots = ["q01", "q02", "q03", "q04", "q05", "q06", "q07", "q08", "q09", "q10", "email_result_k10", "email"]
                for slot in slots:
                    slots_mapped_in_domain.remove(slot)

        send_email = tracker.slots.get("email_result_k10")
        if send_email in ["/deny"]:
            slots_mapped_in_domain.remove("email")

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
            dispatcher.utter_message(text = f"Kessler Psychological Distress Scale (K10) - 10 multiple choice questions.")
            
            
        return {"take_k10":take_k10} 

    
    def validate_q10(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        conversation_id=tracker.sender_id
        name = tracker.get_slot("name")
        age = tracker.get_slot("age")
        feel = tracker.get_slot("feel")
        q01,q02,q03,q04,q05,q06,q07,q08,q09,q10 = tracker.get_slot("q01"),tracker.get_slot("q02"),tracker.get_slot("q03"),tracker.get_slot("q04"),tracker.get_slot("q05"),tracker.get_slot("q06"),tracker.get_slot("q07"),tracker.get_slot("q08"),tracker.get_slot("q09"),tracker.get_slot("q10")
        score = int(q01)+int(q02)+int(q03)+int(q04)+int(q05)+int(q06)+int(q07)+int(q08)+int(q09)+int(q10)
        now = datetime.now()
        

        # Save as csv for all users
        form_results = str(conversation_id)+','+str(name)+","+str(age)+","+str(feel)+","+str(q01)+","+str(q02)+","+str(q03)+","+str(q04)+","+str(q05)+","+str(q06)+","+str(q07)+","+str(q08)+","+str(q09)+","+str(q10)+","+str(score)+","+str(now)+"\n"
        f = open("store/k10_results.csv", "a")
        f.write(form_results)
        f.close()

        result = "Your K10 Test Score is: " + str(score) + "/50\n\n"
        if score >= 10 and score <= 19:
            result = result + "You are likely to be well.\n"
        if score >= 20 and score <= 24:
            result = result + "You are likely to have a mild mental disorder.\n"
        if score >= 25 and score <= 29:
            result = result + "You are likely to have moderate mental disorder.\n"
        if score >= 30 and score <= 50:
            # additional text for severe
            result = result + "You are likely to have a severe mental disorder.\n" #color
        
        #result = result + "If you wish to know more about the K10 Test, follow the link: https://www.tac.vic.gov.au/files-to-move/media/upload/k10_english.pdf \n \n"
        dispatcher.utter_message(text = "Thanks "+str(name or 'guest')+", your answers have been recorded!")
        dispatcher.utter_message(text = result)

        result = "Hello " + str(name) + """, Welcome to SilentMoon!
        
Taking care of your mental health is very vital and we're happy to see that you've taken this step forward in the right direction. Sometimes, external factors can affect us more than we think and can take a toll on our health. It is important to stay compassionate and empathetic in challenging situations towards both, others and ourselves.

What is the K10 test?
The Kessler Psychological Distress Scale (K10) is a simple measure of psychological distress. The K10 scale involves 10 questions about emotional states each with a five-level response scale. The measure can be used as a brief screen to identify levels of distress.
Here are your test results:

""" + str(result) + """
According to the K10 test, the lesser your test score the less you are likely to have a mental disorder. Here is a chart to help you understand the test score better;

K10 Total Score Levels - Level of psychological distress
10-19 - are likely to be well
20-24 - are likely to have a mild mental disorder
25-29 - are likely to have a moderate mental disorder
30-50 - are likely to have a severe mental disorder

If your score is higher than 24, it indicates that you're likely to have a moderate to severe mental disorder in which case we suggest you seek immediate professional help or refer to the sources below.

https://www.opencounseling.com/hotlines-in
https://www.nhp.gov.in/national-mental-health-programme_pg
https://www.who.int/health-topics/mental-health#tab=tab_1

If you wish to know more about the K10 Test, follow the link: https://www.tac.vic.gov.au/files-to-move/media/upload/k10_english.pdf

Wish you the best!

Best regards,
SilentMoon."""

        #dispatcher.utter_message(text = "If you wish to know more about the K10 Test, follow the link: https://www.tac.vic.gov.au/files-to-move/media/upload/k10_english.pdf")
        
        return {"result_k10":result, "email_result_k10":None}
    
    
    def validate_email_result_k10(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        email = tracker.get_slot("email")
        send_email = tracker.get_slot("email_result_k10")
        message = tracker.get_slot("result_k10")
        name = tracker.get_slot("name")
        #message = "Hey, " + str(name) + "! \nHere are your K10 test results: \n" + str(result)
        
        if send_email in ["/affirm"]:
            print("sending email k10")
            if email is not None:
                sent = SendEmail(
                email,
                "[SilentMoon] Your K10 test results are here!",
                message
                )
                if sent is True:
                    dispatcher.utter_message("Thank you. We have sent you an email at {} with your test results and more information.".format(tracker.get_slot("email")))
                else:
                    dispatcher.utter_message(text=f"Something went wrong, please try again.")
                    return {"email":None}

        return {"email_result_k10":send_email}
    
    
    def validate_email(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        email = tracker.get_slot("email")
        send_email = tracker.get_slot("email_result_k10")
        message = tracker.get_slot("result_k10")
        name = tracker.get_slot("name")
        
        if send_email in ["/affirm"]:
            print("sending email k10")
            if email is not None:
                sent = SendEmail(
                email,
                "[SilentMoon] Your K10 test results are here!",
                message
                )
                if sent is True:
                    dispatcher.utter_message("Thank you. We have sent you an email at {} with your test results and more information.".format(tracker.get_slot("email")))
                else:
                    dispatcher.utter_message(text=f"Something went wrong, please try again.")
                    return {"email":None}

            
        return {"email":email}
    


def SendEmail(toaddr,subject,message):
    sent = False
    fromaddr = "redxmentalhealthchatbot@gmail.com"
    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = subject

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    try:
        s.login(fromaddr, "redxlabsilentmoon")
        print("logged in gmail")

        # Converts the Multipart msg into a string
        text = msg.as_string()

        # sending the mail
        s.sendmail(fromaddr, toaddr, text)
        print("Email sent")
        sent = True
    except:
        print("An Error occured while sending email.")
    finally:
        # terminating the session
        s.quit()
    
    return(sent)



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
        ask_gad = tracker.slots.get("ask_gad")
        if mood in ["Anxious"] or ask_gad == True:
            print("GAD7")
            take_gad = tracker.slots.get("take_gad")
            if take_gad in ["/deny"]:
                print("deny GAD7")
                slots = ["gq1", "gq2", "gq3", "gq4", "gq5", "gq6", "gq7", "email_result_gad", "email"]
                for slot in slots:
                    slots_mapped_in_domain.remove(slot)
            
        else:
            print("skipped GAD7")
            slots = ["take_gad", "gq1", "gq2", "gq3", "gq4", "gq5", "gq6", "gq7", "email_result_gad", "email"]
            for slot in slots:
                slots_mapped_in_domain.remove(slot)
        
        send_email = tracker.slots.get("email_result_gad")
        if send_email in ["/deny"]:
            slots_mapped_in_domain.remove("email")

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
            dispatcher.utter_message(text = f"Generalised Anxiety Disorder Assessment (GAD-7) - 7 multiple choice questions.")
            dispatcher.utter_message(text = f"Over the last 2 weeks, how often have you been bothered by any of the following problems?")
            
            
        return {"take_gad":take_gad} 

    def validate_gq7(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        conversation_id=tracker.sender_id
        name = tracker.slots.get("name")
        take_gad = tracker.slots.get("take_gad")
        gq1,gq2,gq3,gq4,gq5,gq6,gq7 = tracker.get_slot("gq1"),tracker.get_slot("gq2"),tracker.get_slot("gq3"),tracker.get_slot("gq4"),tracker.get_slot("gq5"),tracker.get_slot("gq6"),tracker.get_slot("gq7")
        score = int(gq1)+int(gq2)+int(gq3)+int(gq4)+int(gq5)+int(gq6)+int(gq7)
        print(score,"/21")

        result = "Your Generalised Anxiety Disorder Questionnaire \n(GAD-7) Total is: " + str(score) + "/21\n\n"
        if score >= 0 and score <= 4:
            result = result + "You are likely to be well.\n"
        if score >= 5 and score <= 9:
            result = result + "You are likely to have a mild anxiety.\n"
        if score >= 10 and score <= 14:
            # further evaluation is recommended when the score is 10 or greater
            # additional text for severe
            result = result + "You are likely to have moderate anxiety.\n"
        if score >= 15 and score <= 21:
            # further evaluation is recommended when the score is 10 or greater
            # additional text for severe
            result = result + "You are likely to have severe anxiety.\n" #color

        #result = result + "If you wish to know more about the GAD-7 Test, follow the link: https://patient.info/doctor/generalised-anxiety-disorder-assessment-gad-7"
        dispatcher.utter_message(text = "Thanks "+str(name or 'guest')+", your answers have been recorded!")
        dispatcher.utter_message(text = result)
        #dispatcher.utter_message(text = "If you wish to know more about the GAD-7 Test, follow the link: https://patient.info/doctor/generalised-anxiety-disorder-assessment-gad-7")
        
        result = "Hello " + str(name) + """, Welcome to SilentMoon!
        
Taking care of your mental health is very vital and we're happy to see that you've taken this step forward in the right direction. Sometimes, external factors can affect us more than we think and can take a toll on our health. It is important to stay compassionate and empathetic in challenging situations towards both, others and ourselves.
        
What is the GAD-7 test?
The GAD-7 also known as the "generalized anxiety disorder" test comprises 7 questions that help you find out if you might have an anxiety disorder that needs treatment. It calculates how many common symptoms you have and based on your answers suggests where you might be on a scale, from mild to severe anxiety.
Here are your test results:
        
""" + str(result) + """
Here is a chart to help you understand the test score better;

0 - 4 = doing well or normal 
5 - 9 = mild anxiety
10 - 14 = moderate anxiety
15 - 21 = severe anxiety

According to the GAD-7 test, If your score is 10 or higher, or if you feel that anxiety is affecting your daily life, we suggest you seek immediate professional help or refer to the sources below.


https://www.opencounseling.com/hotlines-in
https://www.nhp.gov.in/national-mental-health-programme_pg
https://www.who.int/health-topics/mental-health#tab=tab_1

If you wish to know more about the GAD-7 Test, follow the link: https://patient.info/doctor/generalised-anxiety-disorder-assessment-gad-7

Wish you the best!

Best regards,
SilentMoon."""


        # Save as csv for all users
        now = datetime.now()
        form_results = str(conversation_id)+','+str(name)+","+str(gq1)+","+str(gq2)+","+str(gq3)+","+str(gq4)+","+str(gq5)+","+str(gq6)+","+str(gq7)+","+str(score)+","+str(now)+"\n"
        f = open("store/gad7_results.csv", "a")
        f.write(form_results)
        f.close()

        return {"result_gad":result, "email_result_gad":None}

    
    def validate_email_result_gad(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        email = tracker.get_slot("email")
        send_email = tracker.get_slot("email_result_gad")
        message = tracker.get_slot("result_gad")
        name = tracker.get_slot("name")
        #message = "Hey, " + str(name) + "! \nHere are your GAD-7 test results: \n" + str(result)
        
        if send_email in ["/affirm"]:
            print("sending email gad7")
            if email is not None:
                sent = SendEmail(
                email,
                "[SilentMoon] Your GAD-7 test results are here!",
                message
                )
                if sent is True:
                    dispatcher.utter_message("Thank you. We have sent you an email at {} with your test results and more information.".format(tracker.get_slot("email")))
                else:
                    dispatcher.utter_message(text=f"Something went wrong, please try again.")
                    return {"email":None}

        return {"email_result_gad":send_email}
    
    
    def validate_email(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        email = tracker.get_slot("email")
        send_email = tracker.get_slot("email_result_gad")
        message = tracker.get_slot("result_gad")
        name = tracker.get_slot("name")
        
        if send_email in ["/affirm"]:
            print("sending email gad7")
            if email is not None:
                sent = SendEmail(
                email,
                "[SilentMoon] Your GAD-7 test results are here!",
                message
                )
                if sent is True:
                    dispatcher.utter_message("Thank you. We have sent you an email at {} with your test results and more information.".format(tracker.get_slot("email")))
                else:
                    dispatcher.utter_message(text=f"Something went wrong, please try again.")
                    return {"email":None}
        
        return {"email":email}




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
                        "image_url": "img/core.jpg",
                        "buttons": [ 
                            {
                            "title": "Daily check",
                            "payload": "/main_form",
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
                        "image_url": "img/meditation.jpg",
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
                        "image_url": "img/calm.jpg",
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
                            "url": "ui/img/calm.jpg",
                            "type": "web_url"
                            }
                        ]
                    },
                    {
                        "title": "Screening tools",
                        "subtitle": "Easy-to-use, self-administered patient questionnaires",
                        "image_url": "img/screeningtools.jpg",
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


class ActionQod(Action):
    def name(self) -> Text:
        return "action_qod"
    
    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        #
        #qod = requests.get("https://quotes.rest/quote/random?language=en&limit=1")
        qod = requests.get("https://quotes.rest/qod?language=en")
        #print(qod.text)

        json_qod = qod.json()
        qod = json_qod["contents"]["quotes"][0]["quote"]
        author = json_qod["contents"]["quotes"][0]["author"]
        bg = json_qod["contents"]["quotes"][0]["background"]
        title = json_qod["contents"]["quotes"][0]["title"]
        print(qod+'\n~'+author)

        qna = str(qod+'\n\n~'+author)
        if bg is not None:
            bg = {
            "type": "image",
            "payload": {"src":str(bg)}
            }
        dispatcher.utter_message(text=qna, attachment=bg)


        return[]


class ActionSpotify(Action):
    def name(self) -> Text:
        return "action_spotify"
    
    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        #dispatcher.utter_message(text=f"Here's a playlist that could help you boost your mood!")
        message = {
            "type": "video",
            "payload": {"src":"https://open.spotify.com/embed/playlist/37i9dQZF1DX3rxVfibe1L0?utm_source=generator"}
        }
        dispatcher.utter_message(text="Here's a playlist that could help you boost your mood!",attachment=message)
        return []


class ActionResetAllSlots(Action):

    def name(self) -> Text:
        return "action_reset_all_slots"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        #global tasks, ask_gad, ask_k10
        global ask_k10 
        #tasks = []
        #ask_gad = False
        ask_k10 = True
        return [AllSlotsReset()]



class ActionResetPlanday(Action):

    def name(self) -> Text:
        return "action_reset_planday"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        #
        return [SlotSet("task", None), SlotSet("more_task", None), SlotSet("plan_day", "/affirm")]


class ActionResetMain(Action):

    def name(self) -> Text:
        return "action_reset_main"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        #
        return [SlotSet("sleep_hours", None), SlotSet("blood_test", None), SlotSet("mood", None), SlotSet("mood_intense", None), SlotSet("mood_reason", None), SlotSet("self_harm", None), SlotSet("if_helpful", None)]


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
        global ask_k10
        ask_k10 = True
        return [SlotSet("take_k10", "/affirm"), SlotSet("q01", None), SlotSet("q02", None), SlotSet("q03", None), SlotSet("q04", None), SlotSet("q05", None), SlotSet("q06", None), SlotSet("q07", None), SlotSet("q08", None), SlotSet("q09", None), SlotSet("q10", None), SlotSet("email_result_k10", None)]


class ActionResetGAD(Action):

    def name(self) -> Text:
        return "action_reset_gad"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        #global ask_gad
        #ask_gad = True
        return [SlotSet("ask_gad", True), SlotSet("take_gad", "/affirm"), SlotSet("gq1", None), SlotSet("gq2", None), SlotSet("gq3", None), SlotSet("gq4", None), SlotSet("gq5", None), SlotSet("gq6", None), SlotSet("gq7", None), SlotSet("email_result_gad", None)]


class ActionSaveChat(Action):

    def name(self) -> Text:
        return "action_save_chat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conversation=tracker.events
        conversation_id=tracker.sender_id
        #dispatcher.utter_message("The conversation id is {}".format(conversation_id))
        #print(conversation_id,conversation)
        now = datetime.now()
        import os
        if not os.path.isfile("store/full_chat/"+str(conversation_id)+'.txt'):
            with open("store/full_chat/"+str(conversation_id)+'.txt','w') as file:
                file.write(str(now)+','+str(conversation_id)+"\n")
        chat_data=''
        for i in conversation:
            if i['event'] == 'user':
                chat_data+='User: {}'.format(i['text'])+'\n'
                print('User: {}'.format(i['text']))
            elif i['event'] == 'bot':
                print('Bot: {}'.format(i['text']))
                try:
                    chat_data+='Bot: {}'.format(i['text'])+'\n'
                except KeyError:
                    pass
        else:
            with open("store/full_chat/"+str(conversation_id)+'.txt','a', encoding='utf-8') as file:
                file.write(chat_data+'\n')

        #dispatcher.utter_message(text="All Chats saved.")
        print("All Chats saved.")
        
        return []





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

