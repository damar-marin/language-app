import random
import names
import json
from gtts import gTTS
import nltk
import webbrowser
from deep_translator import GoogleTranslator, MyMemoryTranslator
from pypinyin import pinyin
import re
import soundcard as sc
import soundfile as sf
import threading
import time
import numpy as np
import speech_recognition as sr

r = sr.Recognizer()


from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.audio import SoundLoader


LabelBase.register(name='YRDZST', fn_regular='Files\\chinese.ttf')
LabelBase.register(name='arial', fn_regular='Files\\arial.ttf')
LabelBase.register(name='Akshar_Unicode', fn_regular='Files\\hindi.ttf')
LabelBase.register(name='japanese', fn_regular='Files\\japanese.ttf')
LabelBase.register(name='korean', fn_regular='Files\\korean.ttf')

Builder.load_string('''
<MyLabels>:
    id: label12
    mode: 'rectangle'
    pos_hint:{'center_x': 0.5, 'center_y': .75}
    hint_text: 'Select a text and click on the above Icon'
    halign:'center'
    text: ""
    multiline: True
    readonly: True
    size_hint_x:0.8
    use_bubble:False

<MyTextField>:
    id: textfield12
    mode: 'rectangle'
    hint_text: 'Enter your sentence:'
    multiline: True
    helper_text: "Do your best!"
    pos_hint: {'center_x': 0.5, 'center_y': 0.55}
    size_hint_x:0.8
    use_bubble:False


        
''')



class MyTextField(MDTextField):
    def paste(self, *args):
        self.text=""



class MyLabels(MDTextField):
    pass

with open('Files\\personal_data.json', 'r') as f:
    personal_data = json.load(f)

with open('Files\\stories.json', 'r') as f:
    stories_data = json.load(f)



class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.toggle_button = ToggleButton(text="Dark Mode",
                                          pos_hint={'center_x': 0.5, 'center_y': 0.85},
                                          size_hint=(0.3, 0.04),
                                          on_press=self.toggle_dark_mode)

        self.add_widget(self.toggle_button)

        if personal_data["dark_mode"] == "true":
            self.toggle_button.state="down"
            self.theme_cls.theme_style = "Dark"
        else:
            self.toggle_button.state = 'normal'
            self.theme_cls.theme_style = "Light"



        self.name_field = MDTextField(
            hint_text='Enter your nickname',
            helper_text='Required',
            icon_right='account',
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            size_hint_x=0.8
        )
        self.add_widget(self.name_field)

        self.password_field = MDTextField(
            hint_text='Enter your password',
            helper_text='Required',
            password = True,
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint_x=0.8
        )
        self.add_widget(self.password_field)


        self.show_password_button = MDIconButton(
            icon='eye-off',
            pos_hint={'center_x': 0.85, 'center_y': 0.6},
            on_press=self.toggle_password_visibility
        )
        self.add_widget(self.show_password_button)



        self.login_button = MDRaisedButton(
            text='Login',
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            on_press=self.login,
            md_bg_color=(64/255, 207/255, 39/255, 1)
        )
        self.add_widget(self.login_button)

        self.sign_up_button = MDRaisedButton(
            text='Sign Up',
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            on_press=self.sign_up,
            md_bg_color=(64/255, 207/255, 39/255, 1)
        )
        self.add_widget(self.sign_up_button)

        if personal_data["login"]:
            self.name_field.text= personal_data["login"][0]
            self.password_field.text= personal_data["login"][1]

    def toggle_dark_mode(self, instance):
        print(instance.state)
        if instance.state == "down":
            self.theme_cls.theme_style = "Dark"
            personal_data["dark_mode"] = "true"
        else:
            self.theme_cls.theme_style = "Light"
            personal_data["dark_mode"] = "false"

        with open('Files\\personal_data.json', "w") as outfile:
            json.dump(personal_data, outfile)

    def login(self, instance):
        # Get the values from the text fields
        name = self.name_field.text
        password = self.password_field.text

        print("Hello1")
        # Validate the input
        if not name or not password:
            return

        print("Hello2")
        if personal_data["login"] and name == personal_data["login"][0]:
            if password==personal_data["login"][1]:

                # Display the submitted values in a dialog
                dialog = MDDialog(
                    title='You have successfully logged in!',
                    text=f'Welcome!',
                    buttons=[
                        MDRaisedButton(
                            text='OK',
                            md_bg_color=(64/255, 207/255, 39/255, 1),
                            on_release=lambda x: self.go_to_main_screen(instance),
                            on_press=lambda x: dialog.dismiss()
                        )
                    ]
                )
            else:
                dialog = MDDialog(
                    title='Your password is wrong!',
                    text=f'Please, retry again!',
                    buttons=[
                        MDRaisedButton(
                            text='OK',
                            md_bg_color=(64/255, 207/255, 39/255, 1),
                            on_press=lambda x: dialog.dismiss()
                        )
                    ]
                )
        else:
            dialog = MDDialog(
                title="You don't have an account!",
                text=f'Please, sign up first!',
                buttons=[
                    MDRaisedButton(
                        text='OK',
                        md_bg_color=(64/255, 207/255, 39/255, 1),
                        on_press=lambda x: dialog.dismiss()
                    )
                ]
            )
        dialog.open()

    def sign_up(self, instance):
        # Get the values from the text fields
        name = self.name_field.text
        password = self.password_field.text

        # Validate the input
        if not name or not password:
            return

        if name in personal_data["names"].keys():

            dialog = MDDialog(
                title=f'This name "{name}" is taken!',
                text=f'Please, try another name!',
                buttons=[
                    MDRaisedButton(
                        text='OK',
                        md_bg_color=(64/255, 207/255, 39/255, 1),
                        on_press=lambda x: dialog.dismiss()
                    )
                ]
            )

        else:

            personal_data["login"]=[name, password]
            personal_data["names"][name]=0
            with open('Files\\personal_data.json', "w") as outfile:
                json.dump(personal_data, outfile)

            dialog = MDDialog(
                title='You have successfully signed in!',
                text=f'Welcome!',
                buttons=[
                    MDRaisedButton(
                        text='OK',
                        md_bg_color=(64/255, 207/255, 39/255, 1),
                        on_release=lambda x: self.go_to_main_screen(instance),
                        on_press=lambda x: dialog.dismiss()
                    )
                ]
            )
        dialog.open()


    def toggle_password_visibility(self, *args):
        if self.show_password_button.icon == 'eye-off':
            self.show_password_button.icon = 'eye'
            self.password_field.password=False
        else:
            self.show_password_button.icon = 'eye-off'
            self.password_field.password = True




    def go_to_main_screen(self, instance):
        self.manager.current = "main"

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if personal_data["question"]:
            level= personal_data["question"][0]
            topic = personal_data["question"][1]
            story = personal_data["question"][2]
            language = personal_data["question"][3]
            target_language = personal_data["question"][4]
            selected_story= personal_data["question"][5]

        else:
            level = "Select Level"
            topic = "Select Topic"
            story = "Select Story"
            language = "Your Native Language"
            target_language = "Target Language"
            selected_story = ""


        self.course_label = MDLabel(text='Select your settings and start learning!',
            pos_hint={'center_x': 0.5, 'center_y': .85},
            size_hint_x=.9,
            halign='center')
        self.add_widget(self.course_label)




        self.levels= stories_data.keys()
        self.level_menu_items = [
            {
                "text":i,
                "viewclass": "OneLineListItem",
                "on_press": lambda x= i: self.level_menu_callback(x),
            } for i in self.levels
        ]
        self.level_button = MDRaisedButton(
            text= level,
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y':.75},
            on_press=lambda x: self.level_menu.open(),
            size_hint=(0.05, 0.04)
        )
        self.add_widget(self.level_button)

        self.level_menu = MDDropdownMenu(
            caller=self.level_button,
            items=self.level_menu_items,
            position ="center"
        )





        self.topic_button = MDRaisedButton(
            text=topic,
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': .67},
            on_press=lambda x: self.topic_menu.open(),
            size_hint=(0.05, 0.04)
        )
        self.add_widget(self.topic_button)

        self.topic_menu = MDDropdownMenu(
            caller=self.topic_button,
            items=[],
            position ="center"
        )


        self.selected_story = selected_story
        self.story_button = MDRaisedButton(
            text=story,
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': .59},
            on_press=self.story_condition,
            size_hint=(0.05, 0.04)
        )
        self.add_widget(self.story_button)

        self.story_menu = MDDropdownMenu(
            caller=self.story_button,
            items=[],
            position="center"
        )



        self.selected_language = ""
        self.language = personal_data["languages"]

        self.language_menu_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.language_menu_callback(x),
            } for i in self.language
        ]
        self.language_button = MDRaisedButton(
            text=language,
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': .51},
            on_press=lambda x: self.language_menu.open(),
            size_hint=(0.05, 0.04)
        )
        self.add_widget(self.language_button)

        self.language_menu = MDDropdownMenu(
            caller=self.language_button,
            items=self.language_menu_items,
            position="center"
        )

        self.selected_target_language = ""

        self.target_language_menu_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.target_language_menu_callback(x),
            } for i in self.language
        ]
        self.target_language_button = MDRaisedButton(
            text=target_language,
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': .43},
            on_press=lambda x: self.target_language_menu.open(),
            size_hint=(0.05, 0.04)
        )
        self.add_widget(self.target_language_button)

        self.target_language_menu = MDDropdownMenu(
            caller=self.target_language_button,
            items=self.target_language_menu_items,
            position="center"
        )


        skills= ["Reading", "Listening","Writing","Speaking"]

        self.selected_skill = "Select Skill"

        self.skill_menu_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.skill_menu_callback(x),
            } for i in skills
        ]
        self.skill_button = MDRaisedButton(
            text=self.selected_skill,
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': .35},
            on_press=lambda x: self.skill_menu.open(),
            size_hint=(0.05, 0.04)
        )
        self.add_widget(self.skill_button)

        self.skill_menu = MDDropdownMenu(
            caller=self.skill_button,
            items=self.skill_menu_items,
            position="center"
        )




        self.china_label = MDLabel(text='Living in China?',
                                   pos_hint={'center_x': 0.5, 'center_y': .28},
                                   halign="center")
        self.add_widget(self.china_label)

        self.checkbox = MDCheckbox(active=False,
                                 pos_hint={'center_x': 0.5, 'center_y': .23},
                                 size_hint=(0.05, 0.04))

        self.checkbox.bind(active=self.on_checkbox_active)
        self.add_widget(self.checkbox)




        self.start_button = MDRaisedButton(
            text='START',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': .15},
            on_press= self.go_to_question_screen,
            size_hint=(0.05, 0.04)
        )
        self.add_widget(self.start_button)
        self.score_table_button = MDRaisedButton(
            text='Score Table',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': .05},
            on_press=self.go_to_score_screen,
            size_hint=(0.05, 0.04)
        )
        self.add_widget(self.score_table_button)

    def skill_menu_callback(self, text_item):
        self.skill_button.text = text_item
        self.selected_skill = text_item
        self.skill_menu.dismiss()
        personal_data["skill"]= text_item
        with open('Files\\personal_data.json', "w") as outfile:
            json.dump(personal_data, outfile)
    def on_checkbox_active(self, checkbox, value):
        if value:
            personal_data["china"] = "true"
        else:
            personal_data["china"] = "false"

        with open('Files\\personal_data.json', "w") as outfile:
            json.dump(personal_data, outfile)

    def on_pre_enter(self):

        if personal_data["skill"]:
            self.skill_button.text = personal_data["skill"]

        if personal_data["china"] == "true":
            self.checkbox.active=True
        else:
            self.checkbox.active = False

        if personal_data["dark_mode"] == "true":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"
    def go_to_score_screen(self,instance):
        self.manager.current = "score"
    def target_language_menu_callback(self, text_item):
        self.target_language_button.text = text_item
        self.selected_target_language= text_item
        self.target_language_menu.dismiss()
    def language_menu_callback(self, text_item):
        self.language_button.text = text_item
        self.selected_language= text_item
        self.language_menu.dismiss()
    def story_condition(self, *args):

        if self.level_button.text != 'Select Level' and self.topic_button.text != 'Select Topic':
            if self.level_button.text == "Academic Level" and self.topic_button.text in stories_data["Academic Level"].keys() :
                self.story = stories_data["Academic Level"][self.topic_button.text]
                self.story_menu_items = [
                    {
                        "text": f'Article {i + 1}',
                        "viewclass": "OneLineListItem",
                        "on_release": lambda x=i, kind ="Article" : self.story_menu_callback(x, kind),
                    } for i in range(len(self.story))
                ]

            elif self.topic_button.text in stories_data[self.level_button.text].keys():
                self.story = stories_data[self.level_button.text][self.topic_button.text]
                self.story_menu_items = [
                    {
                        "text": f'Story {i + 1}',
                        "viewclass": "OneLineListItem",
                        "on_release": lambda x=i, kind ="Story": self.story_menu_callback(x,kind),
                    } for i in range(len(self.story))
                ]
            else:
                return
            self.story_menu.items= self.story_menu_items
            self.story_menu.open()
    def story_menu_callback(self, text_item,kind):
        self.story_button.text = f'{kind} {text_item + 1}'
        self.selected_story= self.story[text_item]
        self.story_menu.dismiss()
    def topic_menu_callback(self, text_item):
        self.topic_button.text = text_item
        self.topic_menu.dismiss()
    def level_menu_callback(self, text_item):
        if text_item == "Academic Level":
            self.topic = stories_data["Academic Level"].keys()
            self.topic_menu_items = [
                {
                    "text": i,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=i: self.topic_menu_callback(x),
                } for i in self.topic
            ]
            self.topic_menu.items = self.topic_menu_items

        else:
            self.topic = stories_data[text_item].keys()
            self.topic_menu_items = [
                {
                    "text": i,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=i: self.topic_menu_callback(x),
                } for i in self.topic
            ]
            self.topic_menu.items = self.topic_menu_items


        self.level_button.text = text_item
        self.level_menu.dismiss()
    def go_to_course(self, instance):
        webbrowser.open("https://docs.google.com/document/d/1Xw0hPKYRJn_11phd3Puaet9D8gGW5T8WK2UB0NRSw7I/edit?usp=sharing")


    def go_to_question_screen(self, instance):


        if self.level_button.text !="Select Level"and self.topic_button.text != "Select Topic" and self.story_button.text != "Select Story" and self.language_button.text!="Your Native Language" and self.target_language_button.text != "Target Language" and  self.selected_story !="" and self.skill_button.text != "Select Skill":

            personal_data["question"]=[self.level_button.text, self.topic_button.text, self.story_button.text, self.language_button.text, self.target_language_button.text, self.selected_story]


            with open('Files\\personal_data.json', "w") as outfile:
                json.dump(personal_data, outfile)

            if self.skill_button.text == "Writing":
                self.manager.current = "writing"
            elif self.skill_button.text == "Reading":
                self.manager.current = "reading"
            elif self.skill_button.text == "Listening":
                self.manager.current = "listening"
            elif self.skill_button.text == "Speaking":

                if personal_data["china"] == "true":
                    dialog1 = MDDialog(
                        title='Sorry, You cannot connect with Google in China.\nIf you have VPN, You can open VPN and uncheck "Living in China?" CheckBox.',
                        buttons=[MDRaisedButton(
                            text='OK',
                            md_bg_color=(64/255, 207/255, 39/255, 1),

                            # on_release=lambda x: self.go_to_main_screen(instance),
                            on_press=lambda x: dialog1.dismiss(),

                        )]
                    )
                    dialog1.open()
                    self.manager.current = "main"
                else:
                    self.manager.current = "speaking"

class WritingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.total_score = 0
        self.sentences = [""]
        self.sentence_index = 1
        self.target_language= "Language"
        self.native_language="Native"
        self.language_codes= personal_data["language_codes"]


        self.explainer_label = MDLabel(text= f"Translate the following sentence into {self.target_language[0].upper()+ self.target_language[1:]}.",
                                    size_hint_x=.9,
                                    pos_hint={"center_y":0.95, "top_x":0.5},
                                    halign="center"
                                    )
        self.add_widget(self.explainer_label)
        self.translated_sentence=""


        self.sending_sentence= f"Sentence {self.sentence_index}/{len(self.sentences)}: {self.translated_sentence}"

        self.my_labels = MyLabels()
        self.my_labels.size_hint=(0.9, 0.25)
        self.add_widget(self.my_labels)


        self.my_text_field = MyTextField()
        self.add_widget(self.my_text_field)

        self.back_button = MDRaisedButton(
            text='Back',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.2, 'center_y': .10},
            on_press=self.go_to_main_screen
        )
        self.add_widget(self.back_button)
        self.check_button = MDRaisedButton(
            text='Check',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': .10},
            on_press=self.check_selection
        )
        self.add_widget(self.check_button)


        self.selected_word=""
        self.translate_button = MDIconButton(
            icon='translate',
            pos_hint={'center_x': 0.2, 'center_y': 0.9},
            on_release=self.select_text
        )
        self.add_widget(self.translate_button)

        Clock.schedule_interval(self.print_selected_text,1)

        self.sound = None
        self.text_length=0
    def print_selected_text(self, dt):
        if self.my_labels.selection_text:
            self.selected_word = self.my_labels.selection_text

        if len(self.my_text_field.text)-self.text_length>15:
            self.my_text_field.text=""
            self.text_length = 0
        else:
            self.text_length=len(self.my_text_field.text)



    def check_selection(self, instance):

        if self.my_text_field.text=="":
            return

        dialog = MDDialog(
            auto_dismiss=False,
            size_hint=(.9, .9),
        )
        card = MDCard(orientation="vertical")
        dialog_text = MDTextField(text="",
                                  readonly=True,
                                  multiline=True,
                                  font_name="YRDZST",
                                  size_hint=(.9, .7),
                                  halign="center")

        card.add_widget(dialog_text)

        if personal_data["china"]=="false":
            self.speech_label= MDLabel(text="Click on the below Icon to listen the correct answer." ,
                                       pos_hint={"center_x":0.5,"center_y":0.35},
                                       halign="center",
                                       size_hint=(.8, .02))
            card.add_widget(self.speech_label)
            listen_button = MDIconButton(
                icon='speaker-play',
                halign="center",
                pos_hint={"center_x":0.5,"center_y":0.3},
                on_release=lambda x:text_to_speech()
            )
            card.add_widget(listen_button)



        card.add_widget(MDRaisedButton(
            text='OK',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.8},

            # on_release=lambda x: self.go_to_main_screen(instance),
            on_press=lambda x: dismiss()
        ))
        dialog.add_widget(card)
        dialog.open()

        original_sentence = self.sentences[self.sentence_index - 1]
        native_language_sentence = self.my_labels.text.split("\n\n")[1]
        target_language_sentence = self.my_text_field.text


        if personal_data["china"]=="false":
            correct_answer = GoogleTranslator(source="english",
                                              target=f"{self.target_language}").translate(original_sentence)

            user_answer = GoogleTranslator(source=f"{self.target_language}",
                                           target="english").translate(target_language_sentence)
        else:
            correct_answer = MyMemoryTranslator(self.language_codes["english"],
                                              target=f"{self.language_codes[self.target_language]}").translate(original_sentence)

            user_answer = MyMemoryTranslator(source=f"{self.language_codes[self.target_language]}",
                                           target=self.language_codes["english"]).translate(target_language_sentence)




        distance = nltk.edit_distance(original_sentence, user_answer)
        print(distance)
        similarity = int(10 - (distance / 10))

        self.total_score += similarity



        if "chinese" in personal_data['question'][3]:
            result = ''.join([sublist[0] for sublist in pinyin(self.translated_sentence)])

            text = f' Your score: {similarity}/10\n\n If you finish the whole story, you will get bonus score!\n\n {self.translated_sentence}\n{result}\n\n Your Sentence:\n {target_language_sentence}\n\n Correct Answer: \n{correct_answer}\n '
        elif "chinese" in personal_data['question'][4]:
            result = ''.join([sublist[0] for sublist in pinyin(correct_answer)])

            text = f' Your score: {similarity}/10\n\n If you finish the whole story, you will get bonus score!\n\n {self.translated_sentence}\n\n Your Sentence:\n {target_language_sentence}\n\n Correct Answer: \n{correct_answer}\n{result}\n '

        else:
            text = f' Your score: {similarity}/10\n\n If you finish the whole story, you will get bonus score!\n\n {self.translated_sentence}\n\n Your Sentence:\n {target_language_sentence}\n\n Correct Answer: \n{correct_answer}\n '

        dialog_text.text = text

        if "chinese" in personal_data['question'][4] or "chinese" in personal_data['question'][3]:
            dialog_text.font_name = "YRDZST"

        elif "hindi" == personal_data['question'][4] or "hindi" == personal_data['question'][3]:
            dialog_text.font_name = "Akshar_Unicode"
        elif "japanese" == personal_data['question'][4] or "japanese" == personal_data['question'][3]:
            dialog_text.font_name = "japanese"
        elif "korean" == personal_data['question'][4] or "korean" == personal_data['question'][3]:
            dialog_text.font_name = "korean"
        else:
            dialog_text.font_name = "arial"


        def text_to_speech():
            if self.sound:
                self.sound.play()
                return

            try:
                if "chinese" in self.target_language:
                    language="zh"
                else:
                    language = personal_data["language_codes"][self.target_language].split("-")[0]


                output = gTTS(text=correct_answer, lang=language, slow=True)
                output.save("output.mp3")
                self.sound = SoundLoader.load("output.mp3")

                if self.sound:
                    self.sound.play()
            except:
                self.speech_label.text=f"Sorry, the text in {self.target_language} cannot convert to audio."

        def dismiss():
            dialog.dismiss()
            self.sound=None
            if self.sentence_index== len(self.sentences):

                dialog1 = MDDialog(
                    title=f'CONGRATULATIONS!\n\nYour score from this story: {self.total_score}\n\nYour bonus score: {int(self.total_score/2)}\n\nYour total score: {int(self.total_score+int(self.total_score/2))}',
                    auto_dismiss=False,
                    size_hint=(.9, .9),
                    buttons= [MDRaisedButton(
                        text='OK',
                        md_bg_color=(64/255, 207/255, 39/255, 1),

                        # on_release=lambda x: self.go_to_main_screen(instance),
                        on_press=lambda x: dismiss_dialog1(),

                    )]
                )
                dialog1.open()
                self.total_score += int(self.total_score / 2)
                personal_data["score"] += self.total_score
                with open('Files\\personal_data.json', "w") as outfile:
                    json.dump(personal_data, outfile)
                self.total_score = 0
                def dismiss_dialog1():
                    dialog1.dismiss()
                    self.manager.current = "main"


            else:
                self.sentence_index += 1

                if personal_data["china"] == "false":
                    self.translated_sentence = GoogleTranslator(source="english",
                                                                target=f"{self.native_language}").translate(
                        self.sentences[self.sentence_index - 1])
                else:
                    self.translated_sentence = MyMemoryTranslator(source=self.language_codes["english"],
                                                                  target=f"{self.language_codes[self.native_language]}").translate(
                        self.sentences[self.sentence_index - 1])


                self.sending_sentence = f"Sentence {self.sentence_index}/{len(self.sentences)}:\n\n {self.translated_sentence}"
                self.my_labels.text = self.sending_sentence
                self.my_text_field.text=""


    def on_pre_leave(self):

        personal_data["score"] += self.total_score
        with open('Files\\personal_data.json', "w") as outfile:
            json.dump(personal_data, outfile)

        self.total_score = 0
        self.sentence_index = 1
    def select_text(self,*args):
        self.native_language= personal_data['question'][3]
        self.target_language = personal_data['question'][4]
        selected_text = self.selected_word
        if personal_data["china"] == "false":
            chinese_word = GoogleTranslator(source=f"{self.native_language}",
                                        target=f"{self.target_language}").translate(selected_text)
        else:
            chinese_word = MyMemoryTranslator(source=self.language_codes[self.native_language],
                                                        target=f"{self.language_codes[self.target_language]}").translate(selected_text)


        if "chinese" in personal_data['question'][4]:


            result = ''.join([sublist[0] for sublist in pinyin(chinese_word)])

            self.my_labels.hint_text = f""" >   {chinese_word}   -   {result}   <"""
        else:

            self.my_labels.hint_text = f""" >   {chinese_word}   <"""


    def go_to_main_screen(self, instance):
        self.manager.current = "main"
    def on_pre_enter(self):
        if personal_data["dark_mode"] == "true":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


        self.native_language= personal_data['question'][3]
        self.target_language = personal_data['question'][4]

        text = personal_data["question"][5].replace("\n\n\n", " ").replace("\n\n", " ").replace("\n", " ")
        pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|")(?<!Mrs\.)(?<! Mr\.)(?<! Miss\.)\s'

        self.sentences = re.split(pattern, text)
        self.explainer_label.text= f"Translate the following sentence into {self.target_language[0].upper()+ self.target_language[1:]}."
        self.my_labels.size_hint_x=0.9
        self.my_text_field.size_hint_x = 0.9

        self.my_labels._hint_text_font_size= 20

        try:
            if personal_data["china"]=="false":
                self.translated_sentence = GoogleTranslator(source="english",
                                                            target=f"{self.native_language}").translate(
                    self.sentences[self.sentence_index - 1])
            else:
                self.translated_sentence = MyMemoryTranslator(source=self.language_codes["english"],
                                                            target=f"{self.language_codes[self.native_language]}").translate(
                    self.sentences[self.sentence_index - 1])
        except:
            dialog1 = MDDialog(
                title='You cannot connect with Google Translate.\n Please check "Living in China?" CheckBox.',
                buttons=[MDRaisedButton(
                    text='OK',
                    md_bg_color=(64/255, 207/255, 39/255, 1),

                    # on_release=lambda x: self.go_to_main_screen(instance),
                    on_press=lambda x: dialog1.dismiss(),

                )]
            )
            dialog1.open()
            self.manager.current = "main"


        self.sending_sentence = f"Sentence {self.sentence_index}/{len(self.sentences)}:\n\n {self.translated_sentence}"
        self.my_labels.text =self.sending_sentence



        if "chinese" in personal_data['question'][3]:
            self.my_labels.font_name = "YRDZST"
        elif "hindi" == personal_data['question'][3]:
            self.my_labels.font_name = "Akshar_Unicode"
        elif "japanese" == personal_data['question'][3]:
            self.my_labels.font_name = "japanese"
        elif "korean" == personal_data['question'][3]:
            self.my_labels.font_name = "korean"
        else:
            self.my_labels.font_name = "arial"


        if "chinese" in personal_data['question'][4]:
            self.my_text_field.font_name = "YRDZST"
            self.my_labels.font_name_hint_text = "YRDZST"

        elif "hindi" == personal_data['question'][4]:
            self.my_text_field.font_name = "Akshar_Unicode"
            self.my_labels.font_name_hint_text = "Akshar_Unicode"
        elif "japanese" == personal_data['question'][4]:
            self.my_text_field.font_name = "japanese"
            self.my_labels.font_name_hint_text = "japanese"
        elif "korean" == personal_data['question'][4]:
            self.my_text_field.font_name = "korean"
            self.my_labels.font_name_hint_text = "korean"
        else:
            self.my_text_field.font_name = "arial"
            self.my_labels.font_name_hint_text = "arial"

class ReadingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.total_score = 0
        self.sentences = [""]
        self.sentence_index = 1
        self.target_language= "Language"
        self.native_language="Native"
        self.language_codes= personal_data["language_codes"]


        self.explainer_label = MDLabel(text= f"Translate the following sentence into {self.native_language[0].upper()+ self.native_language[1:]}.",
                                    size_hint_x=.9,
                                    pos_hint={"center_y":0.95, "top_x":0.5},
                                    halign="center"
                                    )
        self.add_widget(self.explainer_label)
        self.translated_sentence=""


        self.sending_sentence= f"Sentence {self.sentence_index}/{len(self.sentences)}: {self.translated_sentence}"

        self.my_labels = MyLabels()
        self.my_labels.size_hint=(0.9, 0.25)
        self.add_widget(self.my_labels)


        self.my_text_field = MyTextField()
        self.add_widget(self.my_text_field)

        self.back_button = MDRaisedButton(
            text='Back',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.2, 'center_y': .10},
            on_press=self.go_to_main_screen
        )
        self.add_widget(self.back_button)
        self.check_button = MDRaisedButton(
            text='Check',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': .10},
            on_press=self.check_selection
        )
        self.add_widget(self.check_button)


        self.selected_word=""
        self.translate_button = MDIconButton(
            icon='translate',
            pos_hint={'center_x': 0.2, 'center_y': 0.9},
            on_release=self.select_text
        )
        self.add_widget(self.translate_button)

        Clock.schedule_interval(self.print_selected_text, 1)

        self.sound = None
        self.text_length=0
    def print_selected_text(self, dt):
        if self.my_labels.selection_text:
            self.selected_word = self.my_labels.selection_text
            # print(self.selected_word)

        if len(self.my_text_field.text)-self.text_length>15:
            self.my_text_field.text=""
            self.text_length = 0
        else:
            self.text_length=len(self.my_text_field.text)



    def check_selection(self, instance):

        if self.my_text_field.text=="":
            return

        dialog = MDDialog(
            auto_dismiss=False,
            size_hint=(.9, .9),
        )
        card = MDCard(orientation="vertical")
        dialog_text = MDTextField(text="hello",
                                  readonly=True,
                                  multiline=True,
                                  font_name="YRDZST",
                                  size_hint=(.9, .7),
                                  halign="center")

        card.add_widget(dialog_text)

        if personal_data["china"]=="false":
            self.speech_label= MDLabel(text="Click on the below Icon to listen." ,pos_hint={"center_x":0.5,"center_y":0.35}, halign="center", size_hint=(.8, .02))
            card.add_widget(self.speech_label)
            listen_button = MDIconButton(
                icon='speaker-play',
                halign="center",
                pos_hint={"center_x":0.5,"center_y":0.3},
                on_release=lambda x:text_to_speech()
            )
            card.add_widget(listen_button)



        card.add_widget(MDRaisedButton(
            text='OK',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.8},

            # on_release=lambda x: self.go_to_main_screen(instance),
            on_press=lambda x: dismiss()
        ))
        dialog.add_widget(card)
        dialog.open()

        original_sentence = self.sentences[self.sentence_index - 1]
        native_language_sentence = self.my_labels.text.replace("\n\n","\n")
        target_language_sentence = self.my_text_field.text


        if personal_data["china"]=="false":
            correct_answer = GoogleTranslator(source="english",
                                              target=f"{self.native_language}").translate(original_sentence)

            user_answer = GoogleTranslator(source=f"{self.native_language}",
                                           target="english").translate(target_language_sentence)
        else:
            correct_answer = MyMemoryTranslator(self.language_codes["english"],
                                              target=f"{self.language_codes[self.native_language]}").translate(original_sentence)

            user_answer = MyMemoryTranslator(source=f"{self.language_codes[self.native_language]}",
                                           target=self.language_codes["english"]).translate(target_language_sentence)









        distance = nltk.edit_distance(original_sentence, user_answer)
        similarity = int(10 - (distance / 10))

        self.total_score += similarity

        if "chinese" in personal_data['question'][4]:
            result = ''.join([sublist[0] for sublist in pinyin(self.translated_sentence)])

            text = f' Your score: {similarity}/10\n\n If you finish the whole story, you will get bonus score!\n\n {self.translated_sentence}\n{result}\n\n Your Sentence:\n {target_language_sentence}\n\n Correct Answer: \n{correct_answer}\n '
        elif "chinese" in personal_data['question'][3]:
            result = ''.join([sublist[0] for sublist in pinyin(correct_answer)])

            text = f' Your score: {similarity}/10\n\n If you finish the whole story, you will get bonus score!\n\n {self.translated_sentence}\n\n Your Sentence:\n {target_language_sentence}\n\n Correct Answer: \n{correct_answer}\n{result}\n '

        else:
            text = f' Your score: {similarity}/10\n\n If you finish the whole story, you will get bonus score!\n\n {self.translated_sentence}\n\n Your Sentence:\n {target_language_sentence}\n\n Correct Answer: \n{correct_answer}\n '

        dialog_text.text = text

        if "chinese" in personal_data['question'][4] or "chinese" in personal_data['question'][3]:
            dialog_text.font_name = "YRDZST"

        elif "hindi" == personal_data['question'][4] or "hindi" == personal_data['question'][3]:
            dialog_text.font_name = "Akshar_Unicode"
        elif "japanese" == personal_data['question'][4] or "japanese" == personal_data['question'][3]:
            dialog_text.font_name = "japanese"
        elif "korean" == personal_data['question'][4] or "korean" == personal_data['question'][3]:
            dialog_text.font_name = "korean"
        else:
            dialog_text.font_name = "arial"


        def text_to_speech():
            if self.sound:
                self.sound.play()
                return

            if "chinese" in self.target_language:
                language="zh"
            else:
                language = personal_data["language_codes"][self.target_language].split("-")[0]
            try:

                output = gTTS(text=self.my_labels.text.split("\n\n")[1], lang=language, slow=True)
                output.save("output.mp3")
                self.sound = SoundLoader.load("output.mp3")

                if self.sound:
                    self.sound.play()
            except:
                self.speech_label.text=f"Sorry, the text in {self.target_language} cannot convert to audio."

        def dismiss():
            dialog.dismiss()
            self.sound=None
            if self.sentence_index== len(self.sentences):

                dialog1 = MDDialog(
                    title=f'CONGRATULATIONS!\n\nYour score from this story: {self.total_score}\n\nYour bonus score: {int(self.total_score/2)}\n\nYour total score: {int(self.total_score+int(self.total_score/2))}',
                    auto_dismiss=False,
                    size_hint=(.9, .9),
                    buttons= [MDRaisedButton(
                        text='OK',
                        md_bg_color=(64/255, 207/255, 39/255, 1),

                        # on_release=lambda x: self.go_to_main_screen(instance),
                        on_press=lambda x: dismiss_dialog1(),

                    )]
                )
                dialog1.open()
                self.total_score += int(self.total_score / 2)
                personal_data["score"] += self.total_score
                with open('Files\\personal_data.json', "w") as outfile:
                    json.dump(personal_data, outfile)
                self.total_score = 0
                def dismiss_dialog1():
                    dialog1.dismiss()
                    self.manager.current = "main"


            else:
                self.sentence_index += 1

                if personal_data["china"] == "false":
                    self.translated_sentence = GoogleTranslator(source="english",
                                                                target=f"{self.target_language}").translate(
                        self.sentences[self.sentence_index - 1])
                else:
                    self.translated_sentence = MyMemoryTranslator(source=self.language_codes["english"],
                                                                  target=f"{self.language_codes[self.target_language]}").translate(
                        self.sentences[self.sentence_index - 1])


                self.sending_sentence = f"Sentence {self.sentence_index}/{len(self.sentences)}:\n\n {self.translated_sentence}"
                self.my_labels.text = self.sending_sentence
                self.my_text_field.text=""


    def on_pre_leave(self):

        personal_data["score"] += self.total_score
        with open('Files\\personal_data.json', "w") as outfile:
            json.dump(personal_data, outfile)

        self.total_score = 0
        self.sentence_index = 1
    def select_text(self,*args):
        self.native_language= personal_data['question'][3]
        self.target_language = personal_data['question'][4]
        selected_text = self.selected_word
        if personal_data["china"] == "false":
            chinese_word = GoogleTranslator(source=f"{self.target_language}",
                                        target=f"{self.native_language}").translate(selected_text)
        else:
            chinese_word = MyMemoryTranslator(source=self.language_codes[self.target_language],
                                                        target=f"{self.language_codes[self.native_language]}").translate(selected_text)
        if "chinese" in personal_data['question'][3]:



            result = ''.join([sublist[0] for sublist in pinyin(chinese_word)])

            self.my_labels.hint_text = f""" >   {chinese_word}   -   {result}   <"""
        else:

            self.my_labels.hint_text = f""" >   {chinese_word}   <"""


    def go_to_main_screen(self, instance):
        self.manager.current = "main"
    def on_pre_enter(self):
        if personal_data["dark_mode"] == "true":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


        self.native_language = personal_data['question'][3]
        self.target_language = personal_data['question'][4]

        text = personal_data["question"][5].replace("\n\n\n", " ").replace("\n\n", " ").replace("\n", " ")
        pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|")(?<!Mrs\.)(?<! Mr\.)(?<! Miss\.)\s'

        self.sentences = re.split(pattern, text)

        self.explainer_label.text= f"Translate the following sentence into {self.native_language[0].upper()+ self.native_language[1:]}."
        self.my_labels.size_hint_x=0.9
        self.my_text_field.size_hint_x = 0.9

        self.my_labels._hint_text_font_size= 20

        try:
            if personal_data["china"]=="false":
                self.translated_sentence = GoogleTranslator(source="english",
                                                            target=f"{self.target_language}").translate(
                    self.sentences[self.sentence_index - 1])
            else:
                self.translated_sentence = MyMemoryTranslator(source=self.language_codes["english"],
                                                            target=f"{self.language_codes[self.target_language]}").translate(
                    self.sentences[self.sentence_index - 1])
        except:
            dialog1 = MDDialog(
                title='You cannot connect with Google Translate.\n Please check "Living in China?" CheckBox.',
                buttons=[MDRaisedButton(
                    text='OK',
                    md_bg_color=(64/255, 207/255, 39/255, 1),

                    # on_release=lambda x: self.go_to_main_screen(instance),
                    on_press=lambda x: dialog1.dismiss(),

                )]
            )
            dialog1.open()
            self.manager.current = "main"


        self.sending_sentence = f"Sentence {self.sentence_index}/{len(self.sentences)}:\n\n {self.translated_sentence}"
        self.my_labels.text =self.sending_sentence



        if "chinese" in personal_data['question'][4]:
            self.my_labels.font_name = "YRDZST"
        elif "hindi" == personal_data['question'][4]:
            self.my_labels.font_name = "Akshar_Unicode"
        elif "japanese" == personal_data['question'][4]:
            self.my_labels.font_name = "japanese"
        elif "korean" == personal_data['question'][4]:
            self.my_labels.font_name = "korean"
        else:
            self.my_labels.font_name = "arial"


        if "chinese" in personal_data['question'][3]:
            self.my_text_field.font_name = "YRDZST"
            self.my_labels.font_name_hint_text = "YRDZST"

        elif "hindi" == personal_data['question'][3]:
            self.my_text_field.font_name = "Akshar_Unicode"
            self.my_labels.font_name_hint_text = "Akshar_Unicode"
        elif "japanese" == personal_data['question'][3]:
            self.my_text_field.font_name = "japanese"
            self.my_labels.font_name_hint_text = "japanese"
        elif "korean" == personal_data['question'][3]:
            self.my_text_field.font_name = "korean"
            self.my_labels.font_name_hint_text = "korean"
        else:
            self.my_text_field.font_name = "arial"
            self.my_labels.font_name_hint_text = "arial"

class ListeningScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.total_score = 0
        self.sentences = [""]
        self.sentence_index = 1
        self.target_language= "Language"
        self.native_language="Native"
        self.language_codes= personal_data["language_codes"]


        self.explainer_label = MDLabel(text= f"Listen and translate the sentence into {self.native_language[0].upper()+ self.native_language[1:]}.",
                                    size_hint_x=.9,
                                    pos_hint={"center_y":0.95, "top_x":0.5},
                                    halign="center"
                                    )
        self.add_widget(self.explainer_label)
        self.translated_sentence=""


        self.sending_sentence= f"Sentence {self.sentence_index}/{len(self.sentences)}: {self.translated_sentence}"

        self.listen_button = MDRaisedButton(
            text='Listen',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': .70},
            on_press=self.listen
        )
        self.add_widget(self.listen_button)


        self.my_text_field = MyTextField()
        self.add_widget(self.my_text_field)

        self.back_button = MDRaisedButton(
            text='Back',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.2, 'center_y': .10},
            on_press=self.go_to_main_screen
        )
        self.add_widget(self.back_button)
        self.check_button = MDRaisedButton(
            text='Check',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': .10},
            on_press=self.check_selection
        )
        self.add_widget(self.check_button)



        Clock.schedule_interval(self.print_selected_text, 1)

        self.sound = None
        self.text_length=0
    def listen(self, instance):
        if self.sound:
            self.sound.play()
            return



        if "chinese" in self.target_language:
            language = "zh"
        else:
            language = personal_data["language_codes"][self.target_language].split("-")[0]
        try:

            output = gTTS(text=self.translated_sentence, lang=language, slow=True)
            output.save("output.mp3")
            self.sound = SoundLoader.load("output.mp3")

            if self.sound:
                self.sound.play()
        except:
            self.listen_button.text = f"Sorry, the text in {self.target_language} cannot convert to audio."

    def print_selected_text(self, dt):

        if len(self.my_text_field.text)-self.text_length>15:
            self.my_text_field.text=""
            self.text_length = 0
        else:
            self.text_length=len(self.my_text_field.text)



    def check_selection(self, instance):

        if self.my_text_field.text=="":
            return

        dialog = MDDialog(
            auto_dismiss=False,
            size_hint=(.9, .9),
        )
        card = MDCard(orientation="vertical")
        dialog_text = MDTextField(text="hello",
                                  readonly=True,
                                  multiline=True,
                                  font_name="YRDZST",
                                  size_hint=(.9, .7),
                                  halign="center")

        card.add_widget(dialog_text)

        if personal_data["china"]=="false":
            self.speech_label= MDLabel(text="Click on the below Icon to listen." ,pos_hint={"center_x":0.5,"center_y":0.35}, halign="center", size_hint=(.8, .02))
            card.add_widget(self.speech_label)
            listen_button = MDIconButton(
                icon='speaker-play',
                halign="center",
                pos_hint={"center_x":0.5,"center_y":0.3},
                on_release=lambda x:text_to_speech()
            )
            card.add_widget(listen_button)



        card.add_widget(MDRaisedButton(
            text='OK',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.8},

            # on_release=lambda x: self.go_to_main_screen(instance),
            on_press=lambda x: dismiss()
        ))
        dialog.add_widget(card)
        dialog.open()

        original_sentence = self.sentences[self.sentence_index - 1]

        target_language_sentence = self.my_text_field.text


        if personal_data["china"]=="false":
            correct_answer = GoogleTranslator(source="english",
                                              target=f"{self.native_language}").translate(original_sentence)

            user_answer = GoogleTranslator(source=f"{self.native_language}",
                                           target="english").translate(target_language_sentence)
        else:
            correct_answer = MyMemoryTranslator(self.language_codes["english"],
                                              target=f"{self.language_codes[self.native_language]}").translate(original_sentence)

            user_answer = MyMemoryTranslator(source=f"{self.language_codes[self.native_language]}",
                                           target=self.language_codes["english"]).translate(target_language_sentence)









        distance = nltk.edit_distance(original_sentence, user_answer)
        similarity = int(10 - (distance / 10))

        self.total_score += similarity

        if "chinese" in personal_data['question'][4]:
            result = ''.join([sublist[0] for sublist in pinyin(self.translated_sentence)])

            text = f' Your score: {similarity}/10\n\n If you finish the whole story, you will get bonus score!\n\n {self.translated_sentence}\n{result}\n\n Your Sentence:\n {target_language_sentence}\n\n Correct Answer: \n{correct_answer}\n '
        elif "chinese" in personal_data['question'][3]:
            result = ''.join([sublist[0] for sublist in pinyin(correct_answer)])

            text = f' Your score: {similarity}/10\n\n If you finish the whole story, you will get bonus score!\n\n {self.translated_sentence}\n\n Your Sentence:\n {target_language_sentence}\n\n Correct Answer: \n{correct_answer}\n{result}\n '

        else:
            text = f' Your score: {similarity}/10\n\n If you finish the whole story, you will get bonus score!\n\n {self.translated_sentence}\n\n Your Sentence:\n {target_language_sentence}\n\n Correct Answer: \n{correct_answer}\n '

        dialog_text.text= text


        if "chinese" in personal_data['question'][4] or "chinese" in personal_data['question'][3]:
            dialog_text.font_name = "YRDZST"

        elif "hindi" == personal_data['question'][4] or "hindi" == personal_data['question'][3]:
            dialog_text.font_name = "Akshar_Unicode"
        elif "japanese" == personal_data['question'][4]or "japanese" == personal_data['question'][3]:
            dialog_text.font_name = "japanese"
        elif "korean" == personal_data['question'][4] or "korean" == personal_data['question'][3]:
            dialog_text.font_name = "korean"
        else:
            dialog_text.font_name = "arial"


        def text_to_speech():
            if self.sound:
                self.sound.play()
                return

            if "chinese" in self.target_language:
                language="zh"
            else:
                language = personal_data["language_codes"][self.target_language].split("-")[0]
            try:

                output = gTTS(text=self.my_labels.text.split("\n\n")[1], lang=language, slow=True)
                output.save("output.mp3")
                self.sound = SoundLoader.load("output.mp3")

                if self.sound:
                    self.sound.play()
            except:
                self.speech_label.text=f"Sorry, the text in {self.target_language} cannot convert to audio."

        def dismiss():
            dialog.dismiss()
            self.sound=None
            if self.sentence_index== len(self.sentences):

                dialog1 = MDDialog(
                    title=f'CONGRATULATIONS!\n\nYour score from this story: {self.total_score}\n\nYour bonus score: {int(self.total_score/2)}\n\nYour total score: {int(self.total_score+int(self.total_score/2))}',
                    auto_dismiss=False,
                    size_hint=(.9, .9),
                    buttons= [MDRaisedButton(
                        text='OK',

                        # on_release=lambda x: self.go_to_main_screen(instance),
                        on_press=lambda x: dismiss_dialog1(),

                    )]
                )
                dialog1.open()
                self.total_score += int(self.total_score / 2)
                personal_data["score"] += self.total_score
                with open('Files\\personal_data.json', "w") as outfile:
                    json.dump(personal_data, outfile)
                self.total_score = 0
                def dismiss_dialog1():
                    dialog1.dismiss()
                    self.manager.current = "main"


            else:
                self.sentence_index += 1

                if personal_data["china"] == "false":
                    self.translated_sentence = GoogleTranslator(source="english",
                                                                target=f"{self.target_language}").translate(
                        self.sentences[self.sentence_index - 1])
                else:
                    self.translated_sentence = MyMemoryTranslator(source=self.language_codes["english"],
                                                                  target=f"{self.language_codes[self.target_language]}").translate(
                        self.sentences[self.sentence_index - 1])

                self.sending_sentence = f"Listen Sentence {self.sentence_index}/{len(self.sentences)}"
                self.listen_button.text = self.sending_sentence
                self.my_text_field.text=""


    def on_pre_leave(self):
        self.sound = None
        personal_data["score"] += self.total_score
        with open('Files\\personal_data.json', "w") as outfile:
            json.dump(personal_data, outfile)

        self.total_score = 0
        self.sentence_index = 1


    def go_to_main_screen(self, instance):
        self.manager.current = "main"
    def on_pre_enter(self):
        if personal_data["dark_mode"] == "true":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


        self.native_language = personal_data['question'][3]
        self.target_language = personal_data['question'][4]

        text = personal_data["question"][5].replace("\n\n\n", " ").replace("\n\n", " ").replace("\n", " ")
        pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|")(?<!Mrs\.)(?<! Mr\.)(?<! Miss\.)\s'

        self.sentences = re.split(pattern, text)

        self.explainer_label.text= f"Listen and translate the sentence into {self.native_language[0].upper()+ self.native_language[1:]}."

        self.my_text_field.size_hint_x = 0.9


        try:
            if personal_data["china"]=="false":
                self.translated_sentence = GoogleTranslator(source="english",
                                                            target=f"{self.target_language}").translate(
                    self.sentences[self.sentence_index - 1])
            else:
                self.translated_sentence = MyMemoryTranslator(source=self.language_codes["english"],
                                                            target=f"{self.language_codes[self.target_language]}").translate(
                    self.sentences[self.sentence_index - 1])
        except:
            dialog1 = MDDialog(
                title='You cannot connect with Google Translate.\n Please check "Living in China?" CheckBox.',
                buttons=[MDRaisedButton(
                    text='OK',
                    md_bg_color=(64/255, 207/255, 39/255, 1),

                    # on_release=lambda x: self.go_to_main_screen(instance),
                    on_press=lambda x: dialog1.dismiss(),

                )]
            )
            dialog1.open()
            self.manager.current = "main"


        self.sending_sentence = f"Listen Sentence {self.sentence_index}/{len(self.sentences)}"
        self.listen_button.text =self.sending_sentence




        if "chinese" in personal_data['question'][3]:
            self.my_text_field.font_name = "YRDZST"


        elif "hindi" == personal_data['question'][3]:
            self.my_text_field.font_name = "Akshar_Unicode"

        elif "japanese" == personal_data['question'][3]:
            self.my_text_field.font_name = "japanese"

        elif "korean" == personal_data['question'][3]:
            self.my_text_field.font_name = "korean"

        else:
            self.my_text_field.font_name = "arial"

class SpeakingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.total_score = 0
        self.sentences = [""]
        self.sentence_index = 1
        self.target_language= "Language"
        self.native_language="Native"
        self.language_codes= personal_data["language_codes"]


        self.explainer_label = MDLabel(text= f"Translate the following sentence into {self.target_language[0].upper()+ self.target_language[1:]}.",
                                    size_hint_x=.9,
                                    pos_hint={"center_y":0.95, "top_x":0.5},
                                    halign="center"
                                    )
        self.add_widget(self.explainer_label)
        self.translated_sentence=""


        self.sending_sentence= f"Sentence {self.sentence_index}/{len(self.sentences)}: {self.translated_sentence}"

        self.my_labels = MyLabels()
        self.my_labels.size_hint=(0.9, 0.25)
        self.my_labels.hint_text=""
        self.add_widget(self.my_labels)


        # self.my_text_field = MyTextField()
        self.my_text_field = MyTextField(mode= 'rectangle',
        hint_text= 'The sentence you said:',
        multiline= True,
        helper_text= "Do your best!",
        pos_hint= {'center_x': 0.5, 'center_y': 0.55},
        size_hint_x=0.8,
        use_bubble= False,
        readonly= True)


        self.add_widget(self.my_text_field)

        self.back_button = MDRaisedButton(
            text='Back',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.2, 'center_y': .10},
            on_press=self.go_to_main_screen
        )
        self.add_widget(self.back_button)
        self.check_button = MDRaisedButton(
            text='Check',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': .10},
            on_press=self.check_selection
        )
        self.add_widget(self.check_button)

        self.speak_button = MDRaisedButton(
            text='Speak',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': .30},
            on_press=self.change_text
        )
        self.add_widget(self.speak_button)





        self.sound = None

    def change_text(self, instance):
        if not hasattr(self, 'recording') or not self.recording:
            self.recording = True
            self.speak_button.text = "Stop Speaking"
            threading.Thread(target=self.start_recording_thread).start()
        else:
            self.recording = False
            self.speak_button.text = "Speak"
            time.sleep(1)
            audio_file = "output.wav"
            with sr.AudioFile(audio_file) as source:
                # Read the audio data from the file
                audio = r.record(source)

                try:
                    # Use the recognizer to convert audio to text
                    text = r.recognize_google(audio, language= personal_data["language_codes"][personal_data["question"][4]])
                    self.my_text_field.text = text
                except sr.UnknownValueError:
                    self.my_text_field.text ="Could not understand audio"
                except sr.RequestError as e:
                    self.my_text_field.text ="Error occurred during speech recognition: {0}".format(e)
    def start_recording_thread(self):
        fs = 44100  # Sample rate

        # Get default input device
        device = sc.default_microphone()

        # Start recording
        print("Recording started...")
        frames = []


        while self.recording:
            # Record audio frames
            frame = device.record(numframes=fs, samplerate=fs, channels=1)
            frames.append(frame)

        # Convert frames to a single ndarray
        recording = np.concatenate(frames)

        # Save recording to a WAV file
        sf.write("output.wav", recording, fs)




    def check_selection(self, instance):

        if self.my_text_field.text=="":
            return

        dialog = MDDialog(
            auto_dismiss=False,
            size_hint=(.9, .9),
        )
        card = MDCard(orientation="vertical")
        dialog_text = MDTextField(text="hello",
                                  readonly=True,
                                  multiline=True,
                                  font_name="YRDZST",
                                  size_hint=(.9, .7),
                                  halign="center")

        card.add_widget(dialog_text)

        if personal_data["china"]=="false":
            self.speech_label= MDLabel(text="Click on the below Icon to listen the correct answer." ,pos_hint={"center_x":0.5,"center_y":0.35}, halign="center", size_hint=(.8, .02))
            card.add_widget(self.speech_label)
            listen_button = MDIconButton(
                icon='speaker-play',
                halign="center",
                pos_hint={"center_x":0.5,"center_y":0.3},
                on_release=lambda x:text_to_speech()
            )
            card.add_widget(listen_button)



        card.add_widget(MDRaisedButton(
            text='OK',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.8},

            # on_release=lambda x: self.go_to_main_screen(instance),
            on_press=lambda x: dismiss()
        ))
        dialog.add_widget(card)
        dialog.open()

        original_sentence = self.sentences[self.sentence_index - 1]
        native_language_sentence = self.my_labels.text.replace("\n\n","\n")
        target_language_sentence = self.my_text_field.text


        if personal_data["china"]=="false":
            correct_answer = GoogleTranslator(source="english",
                                              target=f"{self.target_language}").translate(original_sentence)

            user_answer = GoogleTranslator(source=f"{self.target_language}",
                                           target="english").translate(target_language_sentence)
        else:
            correct_answer = MyMemoryTranslator(self.language_codes["english"],
                                              target=f"{self.language_codes[self.target_language]}").translate(original_sentence)

            user_answer = MyMemoryTranslator(source=f"{self.language_codes[self.target_language]}",
                                           target=self.language_codes["english"]).translate(target_language_sentence)









        distance = nltk.edit_distance(original_sentence, user_answer)
        similarity = int(10 - (distance / 10))

        self.total_score += similarity

        if "chinese" in personal_data['question'][3]:
            result = ''.join([sublist[0] for sublist in pinyin(self.translated_sentence)])

            text = f' Your score: {similarity}/10\n\n If you finish the whole story, you will get bonus score!\n\n {self.translated_sentence}\n{result}\n\n Your Sentence:\n {target_language_sentence}\n\n Correct Answer: \n{correct_answer}\n '
        elif "chinese" in personal_data['question'][4]:
            result = ''.join([sublist[0] for sublist in pinyin(correct_answer)])

            text = f' Your score: {similarity}/10\n\n If you finish the whole story, you will get bonus score!\n\n {self.translated_sentence}\n\n Your Sentence:\n {target_language_sentence}\n\n Correct Answer: \n{correct_answer}\n{result}\n '

        else:
            text = f' Your score: {similarity}/10\n\n If you finish the whole story, you will get bonus score!\n\n {self.translated_sentence}\n\n Your Sentence:\n {target_language_sentence}\n\n Correct Answer: \n{correct_answer}\n '

        dialog_text.text = text

        if "chinese" in personal_data['question'][4] or "chinese" in personal_data['question'][3]:
            dialog_text.font_name = "YRDZST"

        elif "hindi" == personal_data['question'][4] or "hindi" == personal_data['question'][3]:
            dialog_text.font_name = "Akshar_Unicode"
        elif "japanese" == personal_data['question'][4] or "japanese" == personal_data['question'][3]:
            dialog_text.font_name = "japanese"
        elif "korean" == personal_data['question'][4] or "korean" == personal_data['question'][3]:
            dialog_text.font_name = "korean"
        else:
            dialog_text.font_name = "arial"


        def text_to_speech():
            if self.sound:
                self.sound.play()
                return

            if "chinese" in self.target_language:
                language="zh"
            else:
                language = personal_data["language_codes"][self.target_language].split("-")[0]
            try:

                output = gTTS(text=correct_answer, lang=language, slow=True)
                output.save("output.mp3")
                self.sound = SoundLoader.load("output.mp3")

                if self.sound:
                    self.sound.play()
            except:
                self.speech_label.text=f"Sorry, the text in {self.target_language} cannot convert to audio."

        def dismiss():
            dialog.dismiss()
            self.sound=None
            if self.sentence_index== len(self.sentences):

                dialog1 = MDDialog(
                    title=f'CONGRATULATIONS!\n\nYour score from this story: {self.total_score}\n\nYour bonus score: {int(self.total_score/2)}\n\nYour total score: {int(self.total_score+int(self.total_score/2))}',
                    auto_dismiss=False,
                    size_hint=(.9, .9),
                    buttons= [MDRaisedButton(
                        text='OK',
                        md_bg_color=(64/255, 207/255, 39/255, 1),

                        # on_release=lambda x: self.go_to_main_screen(instance),
                        on_press=lambda x: dismiss_dialog1(),

                    )]
                )
                dialog1.open()
                self.total_score += int(self.total_score / 2)
                personal_data["score"] += self.total_score
                with open('Files\\personal_data.json', "w") as outfile:
                    json.dump(personal_data, outfile)
                self.total_score = 0
                def dismiss_dialog1():
                    dialog1.dismiss()
                    self.manager.current = "main"


            else:
                self.sentence_index += 1

                if personal_data["china"] == "false":
                    self.translated_sentence = GoogleTranslator(source="english",
                                                                target=f"{self.native_language}").translate(
                        self.sentences[self.sentence_index - 1])
                else:
                    self.translated_sentence = MyMemoryTranslator(source=self.language_codes["english"],
                                                                  target=f"{self.language_codes[self.native_language]}").translate(
                        self.sentences[self.sentence_index - 1])


                self.sending_sentence = f"Sentence {self.sentence_index}/{len(self.sentences)}:\n\n {self.translated_sentence}"
                self.my_labels.text = self.sending_sentence
                self.my_text_field.text=""


    def on_pre_leave(self):

        personal_data["score"] += self.total_score
        with open('Files\\personal_data.json', "w") as outfile:
            json.dump(personal_data, outfile)

        self.total_score = 0
        self.sentence_index = 1


    def go_to_main_screen(self, instance):
        self.manager.current = "main"
    def on_pre_enter(self):
        if personal_data["dark_mode"] == "true":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


        self.native_language= personal_data['question'][3]
        self.target_language = personal_data['question'][4]

        text = personal_data["question"][5].replace("\n\n\n", " ").replace("\n\n", " ").replace("\n", " ")
        pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|")(?<!Mrs\.)(?<! Mr\.)(?<! Miss\.)\s'

        self.sentences = re.split(pattern, text)

        self.explainer_label.text= f"Translate the following sentence into {self.target_language[0].upper()+ self.target_language[1:]}."
        self.my_labels.size_hint_x=0.9
        self.my_text_field.size_hint_x = 0.9

        self.my_labels._hint_text_font_size= 20

        try:
            if personal_data["china"]=="false":
                self.translated_sentence = GoogleTranslator(source="english",
                                                            target=f"{self.native_language}").translate(
                    self.sentences[self.sentence_index - 1])
            else:
                self.translated_sentence = MyMemoryTranslator(source=self.language_codes["english"],
                                                            target=f"{self.language_codes[self.native_language]}").translate(
                    self.sentences[self.sentence_index - 1])
        except:
            dialog1 = MDDialog(
                title='You cannot connect with Google Translate.\n Please check "Living in China?" CheckBox.',
                buttons=[MDRaisedButton(
                    text='OK',
                    md_bg_color=(64/255, 207/255, 39/255, 1),

                    # on_release=lambda x: self.go_to_main_screen(instance),
                    on_press=lambda x: dialog1.dismiss(),

                )]
            )
            dialog1.open()
            self.manager.current = "main"


        self.sending_sentence = f"Sentence {self.sentence_index}/{len(self.sentences)}:\n\n {self.translated_sentence}"
        self.my_labels.text =self.sending_sentence



        if "chinese" in personal_data['question'][3]:
            self.my_labels.font_name = "YRDZST"
        elif "hindi" == personal_data['question'][3]:
            self.my_labels.font_name = "Akshar_Unicode"
        elif "japanese" == personal_data['question'][3]:
            self.my_labels.font_name = "japanese"
        elif "korean" == personal_data['question'][3]:
            self.my_labels.font_name = "korean"
        else:
            self.my_labels.font_name = "arial"


        if "chinese" in personal_data['question'][4]:
            self.my_text_field.font_name = "YRDZST"
            self.my_labels.font_name_hint_text = "YRDZST"

        elif "hindi" == personal_data['question'][4]:
            self.my_text_field.font_name = "Akshar_Unicode"
            self.my_labels.font_name_hint_text = "Akshar_Unicode"
        elif "japanese" == personal_data['question'][4]:
            self.my_text_field.font_name = "japanese"
            self.my_labels.font_name_hint_text = "japanese"
        elif "korean" == personal_data['question'][4]:
            self.my_text_field.font_name = "korean"
            self.my_labels.font_name_hint_text = "korean"
        else:
            self.my_text_field.font_name = "arial"
            self.my_labels.font_name_hint_text = "arial"

class ScoreScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)





    def on_pre_enter(self):

        for i in range(1, random.randint(2,10)):
            a = names.get_full_name()
            if a not in personal_data["names"].keys():
                personal_data["names"][a]= random.randint(0, max(personal_data["names"].values()))

        name= personal_data["login"][0]
        increment = personal_data["score"]
        if increment>0:
            personal_data["names"][name]+=increment
            for i in personal_data["names"].keys():
                if i !=name:
                    personal_data["names"][i]+= random.randint(0,int(increment*1.3))


        personal_data["score"]=0
        with open('Files\\personal_data.json', "w") as outfile:
            json.dump(personal_data, outfile)

        if personal_data["dark_mode"] == "true":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

        self.my_card = MDCard(orientation="vertical")



        my_dict = personal_data["names"]

        sorted_dict = sorted(my_dict.items(), key=lambda x: x[1], reverse=True)

        # Fetch all rows from the result set
        rows = sorted_dict


        # Create a list to store the data
        score_list = []

        # Iterate over the rows and append data to the list
        index = None
        user_score= None

        for i, row in enumerate(rows):
            name, score = row

            score_list.append(f"{i+1}- {name}: {score}")
            if name ==personal_data["login"][0]:

                index=i
                user_score=score



        self.my_label = MDLabel(text=f"   Your score: {user_score}\n   Your place in the table: {index+1}/{len(rows)} ", size_hint=(.9, .1))
        self.my_card.add_widget(self.my_label)

        updated_score_table=[]
        if len(score_list)<10:
            for i in range(len(score_list)):
                updated_score_table.append(score_list[i])
        elif index<10:
            for i in range(10):
                updated_score_table.append(score_list[i])
        else:

            for i in range(3):
                updated_score_table.append(score_list[i])
            updated_score_table.append("********************")
            for i in range(index-3, index+1):
                updated_score_table.append(score_list[i])
            try:
                for i in range(index+1, index + 3):
                    updated_score_table.append(score_list[i])
            except:
                pass
            index = 7



        # Create the MDList
        self.list_view = MDList()

        # Add OneLineListItems to the MDList
        for i, item in enumerate(updated_score_table):
            if i == index:
                list_item = OneLineListItem(text=item, bg_color=(64/255, 207/255, 39/255, 1))
            else:
                list_item = OneLineListItem(text=item)
            self.list_view.add_widget(list_item)

        # Wrap the MDList in a ScrollView
        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.list_view)
        self.my_card.add_widget(self.scroll_view)

        self.back_main_button = MDRaisedButton(
            text='Back',
            md_bg_color=(64/255, 207/255, 39/255, 1),
            pos_hint={'center_x': 0.5, 'center_y': .10},
            on_press=self.back_main_screen
        )
        self.my_card.add_widget(self.back_main_button)
        self.add_widget(self.my_card)


    def back_main_screen(self,instance):
        self.manager.current = "main"

class MyApp(MDApp):
    def build(self):
        self.title = "Language App"
        self.icon='Files\\icon.ico'
        screen_manager = ScreenManager()


        screen_manager.add_widget(LoginScreen(name="login"))
        screen_manager.add_widget(MainScreen(name="main"))
        screen_manager.add_widget(WritingScreen(name="writing"))
        screen_manager.add_widget(ReadingScreen(name="reading"))
        screen_manager.add_widget(ListeningScreen(name="listening"))
        screen_manager.add_widget(SpeakingScreen(name="speaking"))
        screen_manager.add_widget(ScoreScreen(name="score"))

        return screen_manager

    def on_stop(self):
        screens= ["writing","reading","listening","speaking"]
        for i in screens:
            screen = self.root.get_screen(i)
            personal_data["score"] += screen.total_score
        with open('Files\\personal_data.json', "w") as outfile:
            json.dump(personal_data, outfile)

if __name__ == '__main__':
    MyApp().run()
