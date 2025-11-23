# Patent Center UI

This directory contains the Patent Center UI integration for the Sovereignty Architecture project.

## About

The `index.html` file is the main entry point for the Patent Center web application. It includes:

- **Angular-based UI**: Uses the `<pc-root>` component as the main application container
- **USWDS Design System**: Implements U.S. Web Design System with Public Sans fonts
- **Qualtrics Feedback**: Integrated website feedback collection
- **Session Management**: Session timeout widget for security
- **USPTO Integration**: Dynamic menu components from USPTO

## Monitoring

As of April 22, 2025, Instana monitoring has been removed from this application as it was retired on April 24, 2025. The HTML comments indicate where the Instana scripts were previously located for reference.

## Dependencies

The application requires the following external resources:
- `styles-QIYPFOFU.css` - Main stylesheet
- Various JavaScript chunks and modules (listed in the HTML)
- Font files in `./thirdParty/` directory
- Session timeout widget CSS in `assets/session-timeout-widget/`
- USPTO dynamic menu component

## Usage

This is a static HTML entry point that bootstraps the Angular application. The actual application logic is loaded through the module scripts referenced at the end of the HTML document.
