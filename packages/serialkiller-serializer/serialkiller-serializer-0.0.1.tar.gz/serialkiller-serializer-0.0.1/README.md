# Serialkiller Package

### Introduction
This is a class serialization package. It contains the class
Serializer which can be used to both serialize and deserialize
objects.

### Package usage
Serializer class contains four static methods: ***serialize_,
deserialize_, serialize_many_, deserialize_many_***.

Methods followed by one underline indicates that it is a
static method and must have its arguments fully filled in
order to be called. It also indicates that this method has
"twin" method (same name but without the underline) that
is its partial method, i.e the "twin" method has some or all
arguments preset.

Code example:

    serializer = Serializer(
                    Person,
                    only=['id', 'name', 'age'],
                    ignore=['age']
                )

    person_dict = serializer.serialize(person_1)

    person_2 = serializer.deserialize(
                            {
                                'id': 1,
                                'name': 'MyName',
                                'age': 99
                            }
                        )

The code above shows an example of usage of the Serealizer
class. It serializes ***person_1*** into a ***dict*** and
deserializes the given dict into a Person class object.
Note that the serializer was created to serialize only ***id,
name and age*** attributes, ignoring ***age***. Although it
does not make any practical sense, it shows how the
serializer works. Still one could use this very serializer
discarding the ignoring list, as follows:

    person_dict_full = serializer.serialize_(person_1)

Even though the code above uses the same object created
earlier, note that it uses the ***serialize_*** method.
This time, we did not set ***only*** nor ***ignore*** bounds.

In order to be serialized, a class must have the class
attribute ***\_\_fields__***, as follows:

    class Person:
        __fields__ = ['id', 'name', 'age', 'surname']

        def __init__(id=0, name='', age=0, surname=''):
            self.id = id
            self.name = name
            self.age = age
            self.surname = surname
