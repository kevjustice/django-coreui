<p align="center">
	<a href="https://github.com/kevjustice/django-coreui">
		![Logo](build/DjangoCoreUITemplate/app/static/assets/brand/django-coreui-logo.svg)
	</a>
</p>


<hr>
<h3 align="center">Every site on HTTPS</h3>
<p align="center">Django adaptation of the CoreUI Bootstrap 5 template.</p>
<p align="center">
	<a href="https://github.com/kevjustice/django-coreui/releases">Releases</a> ·
	<a href="https://github.com/kevjustice/django-coreui">Documentation</a>
</p>

### Menu

- [Features](#features)
- [Install](#install)
- [Quick start](#quick-start)
- [Overview](#overview)
- [Full documentation](#full-documentation)
- [Getting help](#getting-help)
- [About](#about)

## Features

- **Get Coding FAST** with a template to jump start your development.
- **Dynamic Menu System** defaults, stored per session, can be dynamically updated!
- **Dynamic Breadcrumbs** Auomatically updated!
- **Dual Theme** including automatic Light/Dark (default is Dark)
- **Sessions** already setup and cached!
- **Custom User Administration** built in.
- **Automatic Admin User** on first run
- **CoreUI** includes [SO MUCH MORE](https://github.com/coreui/coreui-free-bootstrap-admin-template)
    - 

    | Default Theme | 
    | --- | 
    | [![CoreUI PRO Bootstrap Admin Template](https://coreui.io/images/templates/coreui_pro_default_light_dark.webp)](https://coreui.io/product/bootstrap-dashboard-template/?theme=default)

    # CoreUI Icons (522 Free icons) - Premium designed free icon set with marks in SVG, Webfont and raster formats.

    CoreUI Icons are beautifully crafted symbols for common actions and items. You can use them in your digital products for web or mobile app. Ready-to-use fonts and stylesheets that work with your favorite frameworks.

    # Components

    CoreUI Bootstrap Admin Templates are built on top of CoreUI and CoreUI PRO UI components libraries, including all of these components. (Pro items below require CoreUI Pro Licensing.)

    [Bootstrap Accordion](https://coreui.io/bootstrap/docs/components/accordion/)     - [Bootstrap Alert](https://coreui.io/bootstrap/docs/components/alert/)     - [Bootstrap Avatar](https://coreui.io/bootstrap/docs/components/avatar/)   - [Bootstrap Badge](https://coreui.io/bootstrap/docs/components/badge/)     - [Bootstrap Breadcrumb](https://coreui.io/bootstrap/docs/components/breadcrumb/)     - [Bootstrap Button](https://coreui.io/bootstrap/docs/components/button/)     - [Bootstrap Button Group](https://coreui.io/bootstrap/docs/components/button-group/)     - [Bootstrap Callout](https://coreui.io/bootstrap/docs/components/callout/)     - [Bootstrap Card](https://coreui.io/bootstrap/docs/components/card/)     - [Bootstrap Carousel](https://coreui.io/bootstrap/docs/components/carousel/)     - [Bootstrap Checkbox](https://coreui.io/bootstrap/docs/forms/checkbox/)     - [Bootstrap Close Button](https://coreui.io/bootstrap/docs/components/close-button/)     - [Bootstrap Calendar](https://coreui.io/bootstrap/docs/components/calendar/) **PRO**     - [Bootstrap Collapse](https://coreui.io/bootstrap/docs/components/collapse/)     - [Bootstrap Date Picker](https://coreui.io/bootstrap/docs/forms/date-picker/) **PRO**     - [Bootstrap Date Range Picker](https://coreui.io/bootstrap/docs/forms/date-range-picker/) **PRO**     - [Bootstrap Dropdown](https://coreui.io/bootstrap/docs/components/dropdown/)     - [Bootstrap Floating Labels](https://coreui.io/bootstrap/docs/forms/floating-labels/)     - [Bootstrap Footer](https://coreui.io/bootstrap/docs/components/footer/)     - [Bootstrap Header](https://coreui.io/bootstrap/docs/components/header/)     - [Bootstrap Image](https://coreui.io/bootstrap/docs/components/image/)     - [Bootstrap Input](https://coreui.io/bootstrap/docs/forms/input/)     - [Bootstrap Input Group](https://coreui.io/bootstrap/docs/forms/input-group/)     - [Bootstrap List Group](https://coreui.io/bootstrap/docs/components/list-group/)     - [Bootstrap Loading Button](https://coreui.io/bootstrap/docs/components/loading-button/) **PRO**    - [Bootstrap Modal](https://coreui.io/bootstrap/docs/components/modal/)     - [Bootstrap Multi Select](https://coreui.io/bootstrap/docs/forms/multi-select/) **PRO**     - [Bootstrap Navs & Tabs](https://coreui.io/bootstrap/docs/components/navs-tabs/)     - [Bootstrap Navbar](https://coreui.io/bootstrap/docs/components/navbar/)     - [Bootstrap Offcanvas](https://coreui.io/bootstrap/docs/components/offcanvas/)     - [Bootstrap Pagination](https://coreui.io/bootstrap/docs/components/pagination/)     - [Bootstrap Placeholder](https://coreui.io/bootstrap/docs/components/placeholder/)     - [Bootstrap Popover](https://coreui.io/bootstrap/docs/components/popover/)     - [Bootstrap Progress](https://coreui.io/bootstrap/docs/components/progress/)     - [Bootstrap Radio](https://coreui.io/bootstrap/docs/forms/radio/)     - [Bootstrap Range](https://coreui.io/bootstrap/docs/forms/range/)     - [Bootstrap Rating](https://coreui.io/bootstrap/docs/forms/rating/) **PRO**     - [Bootstrap Select](https://coreui.io/bootstrap/docs/forms/select/)     - [Bootstrap Sidebar](https://coreui.io/bootstrap/docs/components/sidebar/)     - [Bootstrap Spinner](https://coreui.io/bootstrap/docs/components/spinner/)     - [Bootstrap Switch](https://coreui.io/bootstrap/docs/forms/switch/)     - [Bootstrap Table](https://coreui.io/bootstrap/docs/components/table/)     - [Bootstrap Textarea](https://coreui.io/bootstrap/docs/forms/textarea/)     - [Bootstrap Time Picker](https://coreui.io/bootstrap/docs/forms/time-picker/) **PRO**     - [Bootstrap Toast](https://coreui.io/bootstrap/docs/components/toast/)     - [Bootstrap Tooltip](https://coreui.io/bootstrap/docs/components/tooltip/)


## Install

```bash
# Create and enter directory
$ git init my-app
$ cd my-app

# Setup sparse-checkout
$ git sparse-checkout init
$ git sparse-checkout set "Build/DjangoCoreUITemplate/app"

# Add remote and pull
$ git remote add origin https://github.com/kevjustice/django-coreui.git
$ git pull origin main

# Setup Python ENV
$ python -m venv venv
$ ./venv/scripts/activate.sh

# Load up requirements
$ pip install --no-cache-dir -r /requirements.txt 
$ cd app

# Apply database migrations
$ python manage.py makemigrations
$ python manage.py migrate

# Start development server
$ python manage.py runserver 0.0.0.0:8000
```