Speaking
========

While radio is often used to distribute music, a common aspect of broadcasting is also the distribution of spoken content.
Since Gencaster aims to be a two-way broadcasting platform, there are several ways to speak in a stream.

Audio files
-----------

One way to speak on the stream is to record yourself or others with a microphone and save the content to an audio file.
Gencaster allows you to play audio files in different formats, but common formats like mp3, wav, opus, AAC or FLAC are supported and recommended.

Gencaster supports two types of playback styles

.. list-table:: Script cell types
    :header-rows: 1
    :widths: 15 30

    * - Playback type
      - Comment
    * - Sync playback
      - The audio file is played in its entirety, and the progress of the graph execution is halted until the file is played in its entirety.
        This is useful for spoken or other sonic content that requires focus from the listener, as it provides a more exclusive space on the stream.
        Using an additional SuperCollider script cell or async audio playback it is possible to provide some background for this playback.
    * - Async playback
      - Once the playback of the file has been started, the execution of the graph will continue.
        This is useful for sonic content which is intended for a background.

        .. todo::

            Currently there is no way to terminate the audio after playback, so once it is running it will be played back until the end.
            At some point the async playback could be attached to a Node scope.


.. admonition:: Action

    * Open the node editor of the *Stop music* node
    * Attach an audio file to it - you can upload one or choose on of the existing files on the server.
      If you upload one, please provide meaningful name for it as you will need to identify the file through its name after the upload.
    * Compare both kinds of playback styles.

Speaking text
-------------

Another way to add a voice to the story graph is to use the text-to-speech engine.
Using an external service that Gencaster can communicate with natively, it is possible to convert a written text into an audible spoken text through a variety of voices and variations.
This allows for more dynamic or generative approaches to text, as the content of the written text can be generated dynamically, as shown in the following chapters.
Also, the conversion of text to speech is very fast, so it is possible to create fast interactions with the listener through text as well.

Any spoken content will block the execution of the graph until the audio file containing the spoken text has been fully played, mimicking the synchronized playback style of an audio file.

.. admonition:: Action

    * Open an arbitrary node of the graph and add a *Markdwon* script cell in it
    * Write some text into it and save the node
    * Listen to it

By building upon `Markdown <https://www.markdownguide.org/basic-syntax/>`_ it is possible to not just declare what needs to be spoken, but also how it needs to be spoken and by whom.

The default voice of Gencaster is ``DE_NEURAL2_C__FEMALE`` - to change the speaker of a section we can wrap the text we want to be spoken by a male person with a special kind of syntax:

.. code:: markdown

    {male}`Wir` müssen auch etwas gemeinsam {male}`sprechen`


It is also possible to change the pronunciation of a word

.. code:: markdown

    Aber bitte, {chars}`bitte`, etwas gelassener.

For a list of all available control statements for text to speech take a look at :ref:`Markdown script cell documentation of the editor<editor_markdown>` and at `SSML <https://cloud.google.com/text-to-speech/docs/ssml>`_.

.. admonition:: Action

    * Modify *how* your written text is spoken.
    * Check the editor documentation and use ``break``

.. note::

    Note that an external service will be used to convert the written text to sound, so the text will have to be transferred to the service provider, who will also charge a fee.
    Creating hours of spoken text is not a problem, as the services are not too expensive, but the mechanisms described can also be used to dynamically generate hundreds of hours of spoken text.

    Since the same Markdown text will always result in the same audio file, we can *cache* the results by storing each result on the server's disk.
    This makes running the graph much faster and cheaper.
    Nevertheless, choose the allocation of your and our resources wisely.
