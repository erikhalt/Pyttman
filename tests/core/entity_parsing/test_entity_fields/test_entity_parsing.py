import decimal
from pyttman.core.containers import Message
from pyttman.core.entity_parsing.fields import (
    BoolEntityField,
    TextEntityField,
    FloatEntityField,
    IntegerEntityField,
    StringEntityField,
    IntEntityField,
    DecimalEntityField
)
from tests.core.entity_parsing.base import (
    ImplementedTestIntent,
    PyttmanInternalTestBaseCase
)
from pyttman.core.entity_parsing.identifiers import (
    NumberIdentifier,
    CapitalizedIdentifier,
    CellPhoneNumberIdentifier,
    DateTimeStringIdentifier
)


class PyttmanIntentInternalEntityParserTestMusicPlayerApp(
    PyttmanInternalTestBaseCase
):
    process_message = True
    mock_message = Message("Play 29 Palms by Robert Plant on Spotify or "
                           "soundCloud and shuffle songs")
    expected_entities = {
        "song": "29 Palms",
        "artist": "Robert Plant",
        "shuffle_songs": True,
        "platform_all": ["Spotify", "soundCloud"],
    }

    class IntentClass(ImplementedTestIntent):
        """
        Test a combination of custom Identifier class for a TextEntityField
        with valid_strings, message_contains all in combinations.
        """
        lead = ("play",)

        exclude = ("on",)
        song = TextEntityField(span=5)
        artist = TextEntityField(prefixes=("by", "with"), span=10,
                                 identifier=CapitalizedIdentifier)

        shuffle_songs = BoolEntityField(message_contains=("shuffle",))

        # Test that both SoundCloud and Spotify are found despite being
        # misspelled in comparison to the mock message above
        # noinspection SpellCheckingInspection
        platform_all = TextEntityField(as_list=True,
                                       span=2,
                                       valid_strings=("spOtifY",
                                                      "soundcloud"))


class PyttmanIntentInternalEntityParserTestTwoTextFields(
    PyttmanInternalTestBaseCase
):
    process_message = True
    mock_message = Message("Adam and Eve were out walking on green grass")
    expected_entities = {
        "person_one": "Adam",
        "person_two": "Eve",
        "grass_color": "green"
    }

    class IntentClass(ImplementedTestIntent):
        """
        Test a combination of custom Identifier class for a TextEntityField
        with valid_strings, message_contains all in combinations.
        """
        valid_strings = ("Adam", "Eve")
        lead = ("walking",)
        person_one = TextEntityField(identifier=CapitalizedIdentifier,
                                     valid_strings=valid_strings)
        person_two = TextEntityField(identifier=CapitalizedIdentifier,
                                     valid_strings=valid_strings)
        grass_color = TextEntityField(suffixes=("grass",))


class PyttmanIntentInternalEntityParserTestTwoTextFieldsWithPrefixes(
    PyttmanInternalTestBaseCase
):
    process_message = True
    mock_message = Message("Adam and Eve were out walking on green grass")
    expected_entities = {
        "person_one_fail": None,
        "person_one": "Adam",
        "person_two": "Eve",
        "grass_color": "green"
    }

    class IntentClass(ImplementedTestIntent):
        """
        Test a combination of custom Identifier class for a TextEntityField
        with valid_strings, message_contains all in combinations.
        prefixed should denote that the entity isn't found.
        """
        valid_strings = ("Adam", "Eve")
        lead = ("walking",)
        person_one_fail = TextEntityField(identifier=CapitalizedIdentifier,
                                          valid_strings=valid_strings,
                                          prefixes=("_prefix_",))
        person_one = TextEntityField(identifier=CapitalizedIdentifier,
                                     valid_strings=valid_strings)
        person_two = TextEntityField(identifier=CapitalizedIdentifier,
                                     valid_strings=valid_strings,
                                     suffixes=("were",))
        grass_color = TextEntityField(suffixes=("grass",))


class PyttmanIntentInternalEntityParserTestBookKeeperApp(
    PyttmanInternalTestBaseCase
):
    process_message = True
    mock_message = Message("add expense Groceries at Whole Foods price 695,"
                           "5684")
    expected_entities = {
        "item": "Groceries",
        "store": "Whole Foods",
        "price": 695.5684,
        "some_undefined": "default"
    }

    class IntentClass(ImplementedTestIntent):
        """
        Tests the Text and Float EntityField classes and performs
        type assertion with prefixes and valid_strings with various
        case miss-matching
        """
        lead = ("new", "add")
        trail = ("expense", "purchase")

        item = TextEntityField(valid_strings=("groceries", "clothes"))
        store = TextEntityField(prefixes=("in", "at", "on"), span=3)
        price = FloatEntityField(prefixes=("price",))
        some_undefined = TextEntityField(prefixes=("none",),
                                         default="default")


class PyttmanIntentInternalEntityParserTestBookKeeperAppWithDecimalField(
    PyttmanIntentInternalEntityParserTestBookKeeperApp
):
    process_message = True
    mock_message = Message("add expense Groceries at Whole Foods price 695,"
                           "5684")
    expected_entities = {
        "item": "Groceries",
        "store": "Whole Foods",
        "price": decimal.Decimal("695.5684"),
        "some_undefined": "default"
    }

    class IntentClass(ImplementedTestIntent):
        """
        Tests the Text and Float EntityField classes and performs
        type assertion with prefixes and valid_strings with various
        case miss-matching
        """
        lead = ("new", "add")
        trail = ("expense", "purchase")

        item = TextEntityField(valid_strings=("groceries", "clothes"))
        store = TextEntityField(prefixes=("in", "at", "on"), span=3)
        price = DecimalEntityField(prefixes=("price",))
        some_undefined = TextEntityField(prefixes=("none",),
                                         default="default")


class PyttmanIntentInternalEntityParserTestTranslatorApp(
    PyttmanInternalTestBaseCase
):
    process_message = True
    mock_message = Message("Translate I Love You from english to swedish")
    expected_entities = {
        "text_to_translate": "I Love You",
        "from_language": "english",
        "to_language": "swedish"}

    class IntentClass(ImplementedTestIntent):
        """
        This test checks using an EntityField as a prefix.
        """
        lead = ("translate",)
        ignore_in_entities = ("to",)
        text_to_translate = TextEntityField(span=100)
        from_language = TextEntityField(prefixes=("from",))
        to_language = TextEntityField(prefixes=(from_language,))


class PyttmanIntentInternalEntityParserTestContactApp(
    PyttmanInternalTestBaseCase
):
    process_message = True
    mock_message = Message("create a new contact Will Byers on mobile with "
                           "0805552859 and do it on 2021-09-20-10:40")
    expected_entities = {
        "contact": "Will Byers",
        "phone_number": "0805552859",
        "phone_standard": "mobile",
        "date_change": "2021-09-20-10:40"}

    class IntentClass(ImplementedTestIntent):
        """
        This test checks DateTimeStringIdentifier used for text, and
        CellphoneIdentifier used for text while simulating a contact app.
        """
        lead = ("create",)
        contact = TextEntityField(identifier=CapitalizedIdentifier, span=2)
        phone_number = TextEntityField(identifier=CellPhoneNumberIdentifier)
        date_change = TextEntityField(identifier=DateTimeStringIdentifier)
        phone_standard = TextEntityField(valid_strings=("mobile",
                                                        "cell",
                                                        "landline"))


class PyttmanIntentInternalEntityParserTestExpenseApp(
    PyttmanInternalTestBaseCase
):
    process_message = True
    test_intent_matching = True
    mock_message = Message("add expense Clothes price 695,5684:-")
    expected_entities = {
        "item": "Clothes",
        "price": 695.5684}

    class IntentClass(ImplementedTestIntent):
        """
        This test checks The TextEntityField, and asserts that the 'default'
        argument works as expected.
        """
        lead = ("new", "add")
        trail = ("expense", "purchase")

        item = TextEntityField(valid_strings=("food", "clothes"),
                               default="default")
        price = FloatEntityField(prefixes=("price",))

        def before_respond(self, message: Message, *args, **kwargs):
            print(f"\nThis was executed before respond")


class PyttmanIntentInternalEntityParserTestWebscraperApp(
    PyttmanInternalTestBaseCase
):
    process_message = True
    mock_message = Message("monitor ManufacturerA ManufacturerB Model123 "
                           "on page_a and page_b price 45000 60 results")
    expected_entities = {
        "manufacturer": "ManufacturerA ManufacturerB",
        "model": "Model123",
        "pages": ["page_a", "page_b"],
        "minimum_price": 45000,
        "create_monitor": True,
        "maximum_results": 60}

    class IntentClass(ImplementedTestIntent):
        """
        This test checks The TextEntityField, and asserts that the 'default'
        argument works as expected.
        """
        lead = ("monitor", "search")
        ignore_in_entities = ("search", "for", "on")
        manufacturer = TextEntityField(span=2)
        model = TextEntityField(prefixes=(manufacturer,))
        pages = TextEntityField(as_list=True,
                                valid_strings=("all", "page_a",
                                               "page_b", "page_c"))
        minimum_price = IntegerEntityField(identifier=NumberIdentifier,
                                           prefixes=("price",))
        maximum_results = IntegerEntityField(suffixes=("results",),
                                             identifier=NumberIdentifier)
        create_monitor = BoolEntityField(message_contains=("monitor", "monitoring"))


def get_valid_strings() -> tuple:
    return "all", "page_a", "page_b", "page_c"


class PyttmanIntentInternalEntityParserTestWebscraperAppWithCallableFields(
    PyttmanInternalTestBaseCase
):
    process_message = True
    mock_message = Message("Search for ManufacturerA ManufacturerB Model123 "
                           "on page_a and page_b price 45000 60 results")
    expected_entities = {
        "manufacturer": "ManufacturerA ManufacturerB",
        "model": "Model123",
        "pages": ["page_a", "page_b"],
        "minimum_price": 45000,
        "maximum_results": 60}

    class IntentClass(ImplementedTestIntent):
        """
        This test checks The TextEntityField, and asserts that the 'default'
        argument works as expected.
        """
        lead = ("Search",)

        # Testing fields with callables instead of hard-coded values
        ignore_in_entities = ("search", "for", "on")
        manufacturer = TextEntityField(span=2)
        model = TextEntityField(prefixes=(manufacturer,))
        pages = TextEntityField(as_list=True,
                                valid_strings=get_valid_strings)
        minimum_price = IntegerEntityField(identifier=NumberIdentifier,
                                           prefixes=("price",))
        maximum_results = IntegerEntityField(suffixes=("results",),
                                             identifier=NumberIdentifier)
        expect_0 = IntegerEntityField(default=0)


class PyttmanIntentInternalEntityParserTestDefaultValues(
    PyttmanInternalTestBaseCase
):
    process_message = True
    mock_message = Message("My new shoes cost me 140:- retail")

    expected_entities = {
        "should_be_foo": "foo",
        "should_be_int_140": 140,
        "should_be_none_str": "None",
        "should_be_0": 0,
        "should_be_42_default_int": 42,
        "purchase_was_retail": True,
    }

    class IntentClass(ImplementedTestIntent):
        """
        This tests that the default values for EntityFields operate as expected.
        """
        lead = ("My",)
        ignore_in_entities = ("My", "new", "shoes", "cost", "me")

        should_be_int_140 = IntEntityField()
        should_be_foo = StringEntityField(default="foo")
        should_be_none_str = StringEntityField(default="None")
        should_be_0 = IntegerEntityField(default=0)
        should_be_42_default_int = IntegerEntityField(default=42)
        purchase_was_retail = BoolEntityField(
            message_contains=("retail",))


class PyttmanIntentInternalTestTrailAndLeadAreNotIgnored(
    PyttmanInternalTestBaseCase
):
    mock_message = Message("Start workshift")
    process_message = True
    expected_entities = {
        "is_workshift": True,
        "is_break": False
    }

    class IntentClass(ImplementedTestIntent):
        """
        Tests that the 'workshift' from 'lead' is not removed
        from parsing, and can be used as entities.
        """
        lead = ("start", "initiate")
        trail = ("workshift", "break")
        exclude_trail_in_entities = False
        exclude_lead_in_entities = False
        exclude_trail = False

        is_break = BoolEntityField(message_contains=("break",))
        is_workshift = BoolEntityField(message_contains=("workshift",))


class PyttmanIntentInternalTestTrailAndLeadAreIgnored(
    PyttmanInternalTestBaseCase
):
    mock_message = Message("Start workshift")
    process_message = True
    expected_entities = {
        "is_workshift": True,
        "is_break": False
    }

    class IntentClass(ImplementedTestIntent):
        """
        Tests that the 'workshift' from 'lead' is not removed
        from parsing, and can be used as entities.
        """
        lead = ("start", "initiate")
        trail = ("workshift", "break")

        is_break = BoolEntityField(message_contains=("break",))
        is_workshift = BoolEntityField(message_contains=("workshift",))


class PyttmanIntentInternalTestTextEntityDefault(
    PyttmanInternalTestBaseCase
):
    mock_message = Message("I would like the blue cheese, please.")
    process_message = True
    expected_entities = {
        "cheese_type": ["blue"],
    }

    class IntentClass(ImplementedTestIntent):
        """
        Tests that the 'workshift' from 'lead' is not removed
        from parsing, and can be used as entities.
        """
        cheese_type = StringEntityField(valid_strings=("blue", "yellow"),
                                        default="blue",
                                        as_list=True)
