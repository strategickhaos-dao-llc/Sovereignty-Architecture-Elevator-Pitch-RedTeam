# Public Web Assets

This directory contains static web assets and applications that can be served publicly.

## MaintenanceFees

The `MaintenanceFees` directory contains the USPTO Fee Processing application, an Angular-based web application for processing United States Patent and Trademark Office maintenance fees.

### Structure

- `index.html` - Main HTML entry point for the Angular application
- The application references additional assets (CSS and JavaScript modules) that would be deployed alongside this file:
  - `styles.*.css` - Application stylesheets
  - `runtime.*.js` - Angular runtime
  - `polyfills.*.js` - Browser polyfills
  - `main.*.js` - Main application bundle

### Features

- Bootstrap 5 styling with CSS custom properties
- Responsive design with viewport optimization
- Print-friendly styling
- Instana monitoring integration
- Angular application framework

### Deployment

This is a static Angular application that can be served by any web server. The base href is set to `/MaintenanceFees/` so the application expects to be served from that path.
