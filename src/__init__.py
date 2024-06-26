from ovos_utils import classproperty
from ovos_utils.process_utils import RuntimeRequirements
from ovos_workshop.intents import IntentBuilder
from ovos_workshop.decorators import intent_handler
# from ovos_workshop.intents import IntentHandler # Uncomment to use Adapt intents
from ovos_workshop.skills import OVOSSkill

# add the home directory to access GasSensor.py
import sys
sys.path.insert(1, '/home/ovos')
from GasSensor import mq2Sensor

# Optional - if you want to populate settings.json with default values, do so here
DEFAULT_SETTINGS = {
    "setting1": True,
    "setting2": 50,
    "setting3": "test"
}

class Mq2Sensor(OVOSSkill):
    def __init__(self, *args, bus=None, **kwargs):
        """The __init__ method is called when the Skill is first constructed.
        Note that self.bus, self.skill_id, self.settings, and
        other base class settings are only available after the call to super().

        This is a good place to load and pre-process any data needed by your
        Skill, ideally after the super() call.
        """
        super().__init__(*args, bus=bus, **kwargs)
        self.sensor = mq2Sensor() # create MQ-2 instance
        self.learning = True

    def initialize(self):
        # merge default settings
        # self.settings is a jsondb, which extends the dict class and adds helpers like merge
        self.settings.merge(DEFAULT_SETTINGS, new_only=True)

    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(
            internet_before_load=False,
            network_before_load=False,
            gui_before_load=False,
            requires_internet=False,
            requires_network=False,
            requires_gui=False,
            no_internet_fallback=True,
            no_network_fallback=True,
            no_gui_fallback=True,
        )

    @property
    def my_setting(self):
        """Dynamically get the my_setting from the skill settings file.
        If it doesn't exist, return the default value.
        This will reflect live changes to settings.json files (local or from backend)
        """
        return self.settings.get("my_setting", "default_value")

    @intent_handler("Sensor.intent")
    def handle_read_sensor(self, message):
        self.log.info("Reading external MQ-2 sensor")
        self.speak_dialog("read_sensor")
        self.speak(str(self.sensor.getSensorVal()) + "ppm")
        if self.sensor.getSensorVal() >= 9000:
            self.speak_dialog("warning_msg")
        self.speak("Recognized by padatious intent handler")

    @intent_handler(IntentBuilder("GasIntent").require("SensorKey"))
    def handle_sensor_adapt_intent(self, message):
        self.log.info("Reading external MQ-2 sensor")
        self.speak_dialog("read_sensor")
        self.speak(str(self.sensor.getSensorVal()) + "ppm")
        if self.sensor.getSensorVal() >= 9000:
            self.speak_dialog("warning_msg")
        self.speak("Recognized by adapt intent handler")

    def stop(self):
        """Optional action to take when "stop" is requested by the user.
        This method should return True if it stopped something or
        False (or None) otherwise.
        If not relevant to your skill, feel free to remove.
        """
        return
