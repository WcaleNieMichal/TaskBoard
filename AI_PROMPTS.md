AI Prompts Documentation

This document contains a collection of useful AI prompts for the TaskBoard project.
Table of Contents

    Introduction

    General Prompts

    Development Prompts

    Testing Prompts

    Dynamic Functionality Prompts

Introduction

This file serves as a central repository for AI prompts that can be used with various AI assistants to support the development, maintenance, and testing of the TaskBoard project.
General Prompts

    After making changes

        Update the documentation in the README.md file.

    Function style

        Functions must be short and perform only one task (Single Responsibility Principle).

    Framework

        The project is based on Flask.

        Use blueprints for API endpoints.

    Documentation

        Generate docstrings in Google style with the following sections:

            Args:

            Returns:

            Raises:

            Examples:

    Updating documentation

        Update the documentation by adding descriptions of endpoints along with example requests and responses.

    Permission Management

        When implementing permission-related features:
            - Always verify user roles and ownership
            - Prevent self-permission removal
            - Use proper HTTP methods (POST for adding, DELETE for removing)
            - Include CSRF protection
            - Add confirmation dialogs for destructive actions
            - Provide clear feedback messages
            - Update UI immediately after successful actions
            - Implement hierarchical permissions (owner > moderator > viewer)
            - Use visual indicators (colors) to show removable users
            - Validate permissions on both frontend and backend

    Blueprint Organization

        When organizing code into blueprints:
            - Separate concerns by functionality (auth, tasks, roles, etc.)
            - Use appropriate URL prefixes for logical grouping
            - Maintain consistent import patterns
            - Keep related forms and routes together
            - Update documentation to reflect new structure

    Dynamic UI Updates

        When implementing dynamic UI functionality:
            - Avoid page refreshes for user actions when possible
            - Use JavaScript classes for complex functionality organization
            - Implement proper error handling and user feedback
            - Use smooth animations and transitions
            - Maintain accessibility standards
            - Ensure graceful degradation for JavaScript-disabled browsers
            - Use event delegation for dynamic elements
            - Implement proper cleanup for event listeners

    Note

        These prompts are intended to ensure consistency of code, documentation, and style throughout the project. AI in Cursor should follow them when generating and refactoring code.

Development Prompts

    Permission Management Development
        - Implement proper error handling for permission operations
        - Use role_required decorator for permission endpoints
        - Follow REST principles for API endpoints
        - Include user feedback for all actions
        - Maintain proper separation of concerns
        - Keep UI responsive and user-friendly

    Dynamic Functionality Development
        - Create modular JavaScript classes for complex interactions
        - Implement proper state management in frontend
        - Use async/await for API calls
        - Handle network errors gracefully
        - Provide immediate visual feedback for user actions
        - Implement optimistic updates with rollback capability
        - Use proper CSRF protection for AJAX requests
        - Maintain separation between UI logic and API communication

    JavaScript Architecture
        - Use ES6+ features (classes, arrow functions, async/await)
        - Implement proper error boundaries
        - Use consistent naming conventions
        - Separate concerns (UI updates, API calls, event handling)
        - Implement proper cleanup for memory leaks prevention
        - Use meta tags for server-side data passing to JavaScript
        - Implement proper loading states for async operations

Testing Prompts

    Permission Testing
        - Test permission removal with various user roles
        - Verify CSRF protection
        - Test error cases (non-existent users, self-removal)
        - Verify UI feedback
        - Test modal confirmation dialog
        - Verify proper role checks

    Dynamic Functionality Testing
        - Test drag and drop functionality across different browsers
        - Verify task updates without page refresh
        - Test dynamic icon visibility based on user permissions
        - Test error handling for network failures
        - Verify proper rollback on server errors
        - Test keyboard accessibility for dynamic elements
        - Verify proper cleanup of event listeners
        - Test performance with large numbers of tasks

    JavaScript Testing
        - Test class initialization and method execution
        - Verify proper event handling and delegation
        - Test async operations and error handling
        - Verify DOM manipulation accuracy
        - Test memory leak prevention
        - Verify proper CSRF token handling in AJAX requests

✅ Ready to use in your project as AI_PROMPTS.md.
Let me know if you want sample development and testing prompts in English tailored for your Flask TaskBoard project for the next step today.