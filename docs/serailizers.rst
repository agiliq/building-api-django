Serializing and Deserializing Data
========================================

DRF makes the process of building web API's simple and flexible. With batteries included,
it comes with well designed base classes which allows us to serialize and deserialize data.


Serialization and Deserialization
--------------------------------------

The first thing we need for our API is to provide a way to serialize model instances into representations. Serialization is the process of making a streamable representation of the data which we can transfer over the network. Deserialization is its reverse process.


Creating Serializers
-----------------------

Lets get started with creating serializer classes which will serialize and deserialize the model instances to json representations. Create a file named :code:`polls/serializers.py`. We will use :code:`ModelSerializer` which will reduce code duplication by automatically determing the set of fields and by creating implementations of the :code:`create()` and :code:`update()` methods.

Our :code:`polls/serializers.py` looks like this.

.. code-block:: python

    from rest_framework import serializers

    from .models import Poll, Choice, Vote


    class VoteSerializer(serializers.ModelSerializer):
        class Meta:
            model = Vote
            fields = '__all__'


    class ChoiceSerializer(serializers.ModelSerializer):
        votes = VoteSerializer(many=True, required=False)

        class Meta:
            model = Choice
            fields = '__all__'


    class PollSerializer(serializers.ModelSerializer):
        choices = ChoiceSerializer(many=True, read_only=True, required=False)

        class Meta:
            model = Poll
            fields = '__all__'


The :code:`PollSerializer` in detail
----------------------------------------

Our :code:`PollSerializer` looks like this.

.. code-block:: python

    ...

    class PollSerializer(serializers.ModelSerializer):
        choices = ChoiceSerializer(many=True, read_only=True, required=False)

        class Meta:
            model = Poll
            fields = '__all__'

What have we got with this? The :code:`PollSerializer` class has a number of methods,

* A :code:`is_valid(self, ..)` method which can tell if the data is sufficient and valid to create/update a model instance.
* A :code:`save(self, ..)` method, which knows how to create or update an instance.
* A :code:`create(self, validated_data, ..)` method which knows how to create an instance. This method can be overriden to customize the create behaviour.
* A :code:`update(self, instance, validated_data, ..)` method which knows how to update an instance. This method can be overriden to customize the update behaviour.


Using the :code:`PollSerializer`
----------------------------------------

Let's use the serializer to create a :code:`Poll` object.

.. code-block:: ipython

    In [1]: from polls.serializers import PollSerializer

    In [2]: from polls.models import Poll

    In [3]: poll_serializer = PollSerializer(data={"question": "Mojito or Caipirinha?", "created_by": 1})

    In [4]: poll_serializer.is_valid()
    Out[4]: True

    In [5]: poll = poll_serializer.save()

    In [6]: poll.pk
    Out[6]: 5


The :code:`poll.pk` line tells us that the object has been commited to the DB. You can also use the serializer to update a :code:`Poll` object. ::


    In [9]: poll_serializer = PollSerializer(instance=poll, data={"question": "Mojito, Caipirinha or margarita?", "created_by": 1})

    In [10]: poll_serializer.is_valid()
    Out[10]: True

    In [11]: poll_serializer.save()
    Out[11]: <Poll: Mojito, Caipirinha or margarita?>

    In [12]: Poll.objects.get(pk=5).question
    Out[12]: 'Mojito, Caipirinha or margarita?'

We can see that calling save on a Serializer with instance causes that instance to be updated. :Code:`Poll.objects.get(pk=5).question` verifies that the Poll was updated.


In the next chapter, we will use the serializers to write views.
