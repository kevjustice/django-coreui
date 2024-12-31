

 
menu template information
    - ELEMENT
        <li class="nav-item"><a class="nav-link" href="index.html">
        <svg class="nav-icon">
            <use xlink:href="/static/modules/@coreui/icons/sprites/free.svg#cil-speedometer"></use>
        </svg> Dashboard<span class="badge badge-sm bg-info ms-auto">NEW</span></a></li>
    - HEADER
        <li class="nav-title">Theme</li>
    - DROPDOWN
        <li class="nav-group"><a class="nav-link nav-group-toggle" href="#">
            <svg class="nav-icon">
            <use xlink:href="/static/modules/@coreui/icons/sprites/free.svg#cil-cursor"></use>
            </svg> Buttons</a>
        <ul class="nav-group-items compact">
            <li class="nav-item"><a class="nav-link" href="buttons/buttons.html"><span class="nav-icon"><span class="nav-icon-bullet"></span></span> Buttons</a></li>
            <li class="nav-item"><a class="nav-link" href="buttons/button-group.html"><span class="nav-icon"><span class="nav-icon-bullet"></span></span> Buttons Group</a></li>
            <li class="nav-item"><a class="nav-link" href="buttons/dropdowns.html"><span class="nav-icon"><span class="nav-icon-bullet"></span></span> Dropdowns</a></li>
            <li class="nav-item"><a class="nav-link" href="https://coreui.io/bootstrap/docs/components/loading-buttons/" target="_blank"><span class="nav-icon"><span class="nav-icon-bullet"></span></span> Loading Buttons
                <svg class="icon icon-sm ms-2">
                <use xlink:href="/static/modules/@coreui/icons/sprites/free.svg#cil-external-link"></use>
                </svg><span class="badge badge-sm bg-danger ms-auto">PRO</span></a></li>
        </ul>
        </li>
menu_authenticated
    - includes "if request.user.is_authenticated"
    - defaults in settings.py
        <li class="nav-item"><a class="nav-link" href="/dashboard">
            <svg class="nav-icon">
            <use xlink:href="/static/modules/@coreui/icons/sprites/free.svg#cil-speedometer"></use>
            </svg> Dashboard</a></li>
            <li class="nav-item"><a class="nav-link" href="/logout">
            <svg class="nav-icon">
                <use xlink:href="/static/modules/@coreui/icons/sprites/free.svg#cil-exit-to-app"></use>
            </svg> Logout</a></li>
menu_un_authenticated
    - defaults in settings.py
        <li class="nav-item"><a class="nav-link" href="/">
            <svg class="nav-icon">
            <use xlink:href="/static/modules/@coreui/icons/sprites/free.svg#cil-home"></use>
            </svg> Home</a></li>
        <li class="nav-item"><a class="nav-link" href="/login">
            <svg class="nav-icon">
            <use xlink:href="/static/modules/@coreui/icons/sprites/free.svg#cil-lock-locked"></use>
            </svg> Login</a></li>
  
top_menu
    - Top of main page
    - template
        <ul class="header-nav d-none d-lg-flex">
            <li class="nav-item"><a class="nav-link" href="/dashboard">Dashboard</a></li>
            <li class="nav-item"><a class="nav-link" href=/users">Users</a></li>
            <li class="nav-item"><a class="nav-link" href="/settings">Settings</a></li>
        </ul>

        ==========================
title
    - page title
    - text only
content: 
    - Page content
page_javascripts
    - Loaded AFTER site_javascripts
    - Full link or style tag (or any combo)
    - should be used for all pages only
    - ex
        <script src="/static/js/myjs.js"></script>
        or
        <script>
            alert('Hello World!');
        </script>     
page_stylesheets
    - loaded AFTER site_stylesheets 
    - Full link or style tag (or any combo)
    - should be used for on specific pages only
    - ex
        <link rel="stylesheet" href="/static/css/mystyles.css">
        or
        <style>
            body {background-color:#fff;}
        </style>