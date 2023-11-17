# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa.shared.core.domain import Domain
from rasa.shared.core.trackers import DialogueStateTracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import graphviz

from pyswip import Prolog
import json
import os.path


class action_default_fallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Disculpame, no entendi bien, podes repetirlo?")
        return []


class manejo_archivo_prolog():
    @staticmethod
    def abrir():
        if os.path.isfile(path="E:/rasa_class/informacion/base_conocimiento.pl"):
            prolog = Prolog()
            prolog = prolog.consult(
                "E:/rasa_class/informacion/base_conocimiento.pl")
            return prolog
        return None


class manejo_archivo_viajes():
    @staticmethod
    def cargar():
        if os.path.isfile(path="E:/rasa_class/informacion/viajes.json"):
            with open('E:/rasa_class/informacion/viajes.json', 'r') as archivo_carga:
                ret = json.load(archivo_carga)
                archivo_carga.close()
        else:
            ret = {}
        return ret


class manejo_archivo_usuarios():
    @staticmethod
    def cargar():
        if os.path.isfile(path="E:/rasa_class/informacion/usuarios.json"):
            with open('E:/rasa_class/informacion/usuarios.json', 'r') as archivo_carga:
                ret = json.load(archivo_carga)
                archivo_carga.close()
        else:
            ret = {}
        return ret

    @staticmethod
    def guardar(Guardar):
        with open('E:/rasa_class/informacion/usuarios.json', 'w') as archivo_guardar:
            json.dump(Guardar, archivo_guardar)
        archivo_guardar.close()


def clean_name(name):
    cleaned_chars = [c if c.isalpha() or c.isspace() else '' for c in name]
    return ''.join(cleaned_chars)


def clean_number(number):
    cleaned_numbers = [c for c in number if c.isdigit()]
    cleaned_number_str = ''.join(cleaned_numbers)

    if cleaned_number_str:
        return int(cleaned_number_str)
    else:
        return 0  # O puedes retornar otro valor predeterminado si lo prefieres


class validar_trip_form(FormValidationAction):
    def name(self) -> Text:
        return "validate_trip_form"

    def validate_name(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        """Validacion del valor de 'name'"""
        name = clean_name(slot_value)

        if len(name) == 0:
            dispatcher.utter_message(text="Disculpame, no te entendi")
            return {"name": None}
        return {"name": name}

    def validate_destination(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        """Validacion del valor de 'destination'"""

        destination = clean_name(slot_value)
        prolog = Prolog()
        prolog.consult('E:/rasa_class/informacion/base_conocimiento.pl')
        if len(destination) == 0:
            dispatcher.utter_message(
                text="Sin el destino no puedo buscarte un paquete de viaje")
        else:
            if list(prolog.query(f"es_ciudad('{str(destination).lower()}')")):
                return {"destination": destination}
            dispatcher.utter_message(
                text=f"Disculpa, no disponemos ofertas turisticas en {destination}.")
        return {"destination": None}

    def validate_budget(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        """Validacion del valor de 'budget'"""

        budget = int(clean_number(slot_value))
        if (budget == 0):
            dispatcher.utter_message(
                text="Necesito un valor de presupuesto valido\npor lo menos un aproximado.")
            return {"budget": None}
        return {"budget": budget}

    def validate_duration(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        """Validacion del valor de 'duration'"""

        duration = int(clean_number(slot_value))

        if (duration == 0):
            dispatcher.utter_message(
                text="Necesito un numero de dias valido\npor lo menos un aproximado.")
            return {"duration": None}
        return {"duration": duration}

    def validate_accommodament(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        """Validacion del valor de 'accommodament'"""
        accommodament = clean_name(slot_value)
        prolog = Prolog()
        prolog.consult('E:/rasa_class/informacion/base_conocimiento.pl')

        if ((len(accommodament) == 0)):
            dispatcher.utter_message(text="Disculpame, no te entendi")
        else:
            if list(prolog.query(f"es_alojamiento('{str(accommodament).lower()}')")):
                return {"accommodament": accommodament}
            dispatcher.utter_message(
                f"No disponemos del alojamiento '{accommodament}', por favor dinos otro.")
        return {"accommodament": None}


class devolver_viajes(Action):
    def name(self) -> Text:
        return "devolver_viajes"

    # Si le interesa por cercania (hacer...)
    # def devolver_viajes_cercanos():

    # Si hizo el formulario
    def devolver_viajes_consulta(self, dispatcher, tracker) -> List[Dict[Text, Any]]:
        destino = tracker.get_slot("destination")
        dias = tracker.get_slot("duration")
        presupuesto = tracker.get_slot("budget")
        alojamiento = tracker.get_slot("accommodament")

        viajes_coincidentes = []
        if destino and dias and presupuesto and alojamiento:
            data_viajes = manejo_archivo_viajes.cargar()
            for viaje in data_viajes['viajes']:
                if (
                    str(viaje['ciudad_destino']).lower() == destino.lower() and
                    viaje["precio"] <= presupuesto and
                    viaje["dias"] == dias and
                    str(viaje["alojamiento"]).lower() == alojamiento.lower()
                ):
                    viajes_coincidentes.append(viaje)

        return viajes_coincidentes

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        viajes = self.devolver_viajes_consulta(dispatcher, tracker)
        if not viajes:
            dispatcher.utter_message(
                "Sepa disculparnos, no tenemos viajes disponibles para usted.")
        else:
            cantidad = 1
            mensaje_viajes = "Aquí están los viajes disponibles:\n"
            for viaje in viajes:
                mensaje_viajes += f"{cantidad}. Destino: {viaje['ciudad_destino']}, Duración: {viaje['dias']} días, Precio: ${viaje['precio']}, Alojamiento: {viaje['alojamiento']}\n"
                cantidad += 1
            dispatcher.utter_message(text=mensaje_viajes)

        return []


class obtener_trayecto(Action):  # PRUEBA
    def name(self) -> Text:
        return "obtener_trayecto"

    def train_tree(self):
        df = pd.read_csv('e:/rasa_class/informacion/data_arbol_decision.csv')
        df = df.drop(columns='id_usuario')

        print(df.sample(5))
        print('..................................')
        print(df.info())
        print('..................................')

        # TRANSFORMAR LOS DATOS
        df = pd.get_dummies(data=df, drop_first=False)
        print(df.sample(5))

        x = df.drop(columns='waze')  # features
        y = df['waze']  # target
        print('..................................')
        print(x.info())
        print('..................................')

        # ENTRENAMIENTO DEL ARBOL DE DECISION

        # Creacion del modelo
        model = DecisionTreeClassifier(max_depth=4)
        # Entrenamiento del modelo
        model.fit(x, y)
        # ¿Que tan bien predice?
        print(model.score(x, y))

        # VISUALIZACION DEL ARBOL

        dot_data = tree.export_graphviz(model, out_file=None,
                                        feature_names=x.columns.tolist(),
                                        class_names=df['waze'].astype(
                                            str).unique().tolist(),
                                        filled=True, rounded=True,
                                        special_characters=True)
        graph = graphviz.Source(dot_data)
        graph.render("E:/rasa_class/informacion/arbolPreview")
        return model

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        model = self.train_tree()  # Entrenamos el Arbol y creamos un modelo.
        edad = next(tracker.get_latest_entity_values('edad'))
        vehiculo = next(tracker.get_latest_entity_values('vehiculo'))
        gama_celular = next(tracker.get_latest_entity_values('gama_celular'))

        if (edad == None):
            dispatcher.utter_message(text="No entiendo la edad")
            return []
        if (vehiculo == None):
            dispatcher.utter_message(
                text="No entiendo si vas en un vehiculo particular o en un colectivo (por ejemplo)")
            return []
        if (gama_celular == None):
            dispatcher.utter_message(text="No entiendo la gama de tu celular")
            return []

        # TRANSFORMACION DE DATOS DE USUARIO

        edad = str(edad)
        vehiculo = vehiculo.lower()
        gama_celular = gama_celular.lower()

        vehiculo = "1" if vehiculo == "particular" else "0"
        gama_celular_baja = "1" if gama_celular == "baja" else "0"
        gama_celular_media = "1" if gama_celular == "media" else "0"
        gama_celular_alta = "1" if gama_celular == "alta" else "0"
        gama_celular_no_se = "1" if gama_celular == "no se" else "0"

        user_data = pd.DataFrame({
            'edad': [edad],
            'vehiculo': [vehiculo],
            'gama_celular_alta': [gama_celular_alta],
            'gama_celular_baja': [gama_celular_baja],
            'gama_celular_media': [gama_celular_media],
            'gama_celular_no se': [gama_celular_no_se]
        })

        y_predict = model.predict(user_data)

        if (y_predict[0] == 1):
            dispatcher.utter_message(
                text="Te recomiendo buscar eso en la aplicacion Waze o en su pagina web https://www.waze.com/es y utilizar su ruta para guiarte mas facil en el mapa")
        else:
            dispatcher.utter_message(
                text="Te recomiendo buscar el trayecto por Google Maps (se puede desde ingresar desde Chrome u otro navegador)")

        return []
