
Bootstrap 4 files for miyadaiku static site generator
========================================================

Provides `Bootstrap4 <https://getbootstrap.com/>`__ 4.4.1 CSS and Javascript files.


Installation
-------------------

Use pip command to install Bootstrap 4. 

::

   $ pip3 install miyadaiku_theme_bootstrap4



Configuraion
----------------------


In your config.yml file of your project, add following configuration at `themes` section.

::

   themes:
     - miyadaiku_theme_bootstrap4    # <---- add this line


Usage
----------------------

Add following code to your template files.

::

  <!-- include boolstrap4 -->
  {{ bootstrap4.load_css(page) }}

  <!-- include jquery.js -->
  {{ jquery.load_js(page) }}

  <!-- include popper.js -->
  {{ popper_js.load_js(page) }}

  <!-- include boolstrap4 js -->
  {{ bootstrap4.load_js(page) }}


Example
-------------

https://github.com/miyadaiku/miyadaiku-docs/tree/master/samples/bootstrap4

