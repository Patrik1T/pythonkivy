# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
#math se zde používá pro pomocí s výpočtem sinusu, cosinusu, tangensu a cotangensu
import math


class Calculator(BoxLayout):
    #**kwargs je klíčový argument a slouží pro vložení neomezeno nových hodnot, které nejsou specifikovány
    def __init__(self, **kwargs):
        #Volání v konstruktoru třídy zavolá konstruktor nadřazené třídy a předá mu případné dodatečné argumenty.
        super(Calculator, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Vytvoření vstupního pole pro výsledky a historii výpočtů
        self.result = TextInput(font_size=32, multiline=False, readonly=True, halign='right', padding=[5, 10])
        self.history = []  # Nový seznam pro uchovávání historie výpočtů
        self.add_widget(self.result)

        # Definice tlačítek pro kalkulačku
        buttons = [
            ['7', '8', '9', '/', '<-', '^'],
            ['4', '5', '6', '*', '(', ')'],
            ['1', '2', '3', '-', '[', ']'],
            ['.', '0', '=', '+', '{', '}'],
            ['sin', 'cos', 'tan', 'cot', 'pi', '%'],
            ['restart', '^2', '√', 'ON/OFF', 'History']
        ]

        # Vytvoření rozvržení tlačítek a jejich přiřazení funkcí
        for row in buttons:
            h_layout = BoxLayout(spacing=5)
            for label in row:
                button = Button(text=label, pos_hint={'center_x': 0.5, 'center_y': 0.5})
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            self.add_widget(h_layout)

        # Nastavení počátečního stavu kalkulačky
        self.calculator_enabled = True

    def on_button_press(self, instance):
        # Ověřuje, zda je kalkulačka povolena a zda stisknuté tlačítko není mimo povolené operace.
        if not self.calculator_enabled and instance.text not in ('ON/OFF', 'C', 'History'):
            return

        current_text = self.result.text  # Ukládá aktuální text zobrazený v kalkulačce.

        # Reakce na stisk různých tlačítek včetně operací a funkcí.
        if instance.text == 'restart':
            self.result.text = ''  # Vymaže obsah kalkulačky.
        elif instance.text == '=':
            try:
                result = str(eval(current_text))  # Vypočítá výraz a převede výsledek na řetězec.
                self.result.text = result  # Zobrazí výsledek.
                self.history.append(f'{current_text} = {result}')  # Přidá výsledek do historie.
            except Exception:
                self.result.text = 'ERROR'  # V případě chyby zobrazí chybu.
        elif instance.text == '<-':
            self.result.text = current_text[:-1]  # Smaže poslední znak v textu.
        elif instance.text == '^':
            # Odstraní poslední operátor nebo závorku ze vstupu.
            last_num_pos = max(current_text.rfind('+'), current_text.rfind('-'), current_text.rfind('*'),
                               current_text.rfind('/'), current_text.rfind('('), current_text.rfind('['),
                               current_text.rfind('{'))
            if last_num_pos == -1:
                self.result.text = ''  # Pokud není nic k odstranění, vymaže text.
            else:
                self.result.text = current_text[:last_num_pos + 1]  # Jinak odstraní poslední číslo nebo operátor.
        elif instance.text in ('sin', 'cos', 'tan', 'cot', 'pi'):
            if instance.text == 'pi':
                self.result.text += '3.14159265'  # Přidá hodnotu pi k aktuálnímu textu.
            else:
                # Zpracuje matematické funkce pomocí math modulu.
                function_mapping = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'cot': lambda x: 1 / math.tan(x)}
                function = function_mapping[instance.text]
                try:
                    # Získá poslední číslo nebo výraz a aplikuje na něj zvolenou funkci.
                    last_num_pos = max(current_text.rfind('+'), current_text.rfind('-'), current_text.rfind('*'),
                                       current_text.rfind('/'), current_text.rfind('('), current_text.rfind('['),
                                       current_text.rfind('{'))
                    if last_num_pos == -1:
                        number = current_text
                    else:
                        number = current_text[last_num_pos + 1:]
                    result = str(function(eval(number)))
                    # Nahradí původní výraz novým výsledkem.
                    self.result.text = result
                    #zachytává všechny výjimky (chyby), které mohou nastat v bloku kódu uvnitř
                except Exception:
                    self.result.text = 'ERROR'  # V případě chyby zobrazí chybu.
        elif instance.text == '%':
            self.result.text += '/100'  # Přidá '/100' k aktuálnímu textu pro výpočet procent.
        elif instance.text == '^2':
            self.result.text += '**2'  # Přidá '**2' k aktuálnímu textu pro výpočet druhé mocniny.
        elif instance.text == '√':
            self.result.text += '**0.5'  # Přidá '**0.5' k aktuálnímu textu pro výpočet odmocniny.
        elif instance.text == 'History':
            # Zobrazí historii výpočtů v popup okně.
            history_str = '\n'.join(self.history)
            # Tato část kódu vytváří vyskakovací okno, se zobrazenou historií výpočtů
            popup = Popup(title='Historie výpočtů', content=TextInput(text=history_str, readonly=True),
                          size_hint=(None, None), size=(400, 400))
            popup.open()
        elif instance.text == 'ON/OFF':
            self.calculator_enabled = not self.calculator_enabled  # Přepíná stav kalkulačky.
            if self.calculator_enabled:
                self.result.text = ''  # Pokud je povolena, vymaže text.
                self.result.readonly = False  # A aktivuje možnost úpravy textu.
            else:
                self.result.text = 'OFF'  # Pokud je vypnuta, zobrazí 'OFF'.
                self.result.readonly = True  # A zakáže úpravu textu.
        else:
            # Pokud je na konci výrazu znak '=', nahradí ho stisknutou hodnotou, jinak přidá hodnotu k aktuálnímu textu.
            if current_text.endswith('='):
                self.result.text = instance.text
            else:
                self.result.text += instance.text

#sestaví se naše kalkulačka za pomocí kivy za metody build
class CalculatorApp(App):
    def build(self):
        return Calculator()


if __name__ == '__main__':
    CalculatorApp().run()