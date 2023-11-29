=========================
List of predefined colors
=========================

The following table lists all the colors which are predefined in this package. The first column shows the color's name
which can be used to retrieve the :py:class:`~physiscript.utils.Color` object using the
:py:meth:`~physiscript.utils.Color.get` or :py:meth:`~physiscript.utils.Color.create` methods. For example:

.. code-block:: python

    c = Color.get("red")

All those names are returned by the :py:meth:`~physiscript.utils.Color.names` method.

The second column shows the constant name of the colors. Each color can be obtained simply by using this constant name.
For example, the above line is equivalent to:

.. code-block:: python

    c = Color.RED

.. raw:: html

   <table class="table">
     <tr>
       <th><p>Color name</p></th>
       <th><p>Constant name</p></th>
       <th><p>RGB</p></th>
       <th><p>HTML code</p></th>
       <th><p>Color</p></th>
     </tr>
   {% for name, color in default_colors.items() %}
     <tr>
       <td><p>{{ name }}</p></td>
       <td><code>{{ name.upper().replace("-", "_") }}</code></td>
       <td><code>rgb{{ color.rgb() }}</code></td>
       <td><code>{{ color.html(include_alpha=False) }}</code></td>
       <td style="background-color: {{ color.html(include_alpha=False) }}"></td>
     </tr>
   {% endfor %}
   </table>
