Core Features

    Code Editing:
        Syntax Highlighting: Supports syntax highlighting for HTML/XML content using the Pygments library. Highlighting colors change based on the active theme (light or dark).
        Auto-Completion: Provides auto-completion for HTML tags and attributes using QCompleter. A list of common HTML tags and attributes is included.
        Code Snippets: Pre-defined snippets for common HTML structures such as <!DOCTYPE html>, <table>, <div>, and more. Snippets can be inserted by selecting them from the context menu or typing the trigger word and pressing Tab.

    File Handling:
        Open and Save Files: Users can open and save HTML or XML files via a file dialog. The editor supports both Ctrl+O (open) and Ctrl+S (save) shortcuts.
        Save As: Users can save the current content as a new file using the "Save As" option.

    Line Numbering:
        A line number area is displayed to the left of the editor to help users keep track of their position in the document.

    Live Preview:
        The code editor has a live preview feature that renders HTML content in a preview pane using QWebEngineView. The preview updates in real time as the user types, with a 300ms debounce to avoid excessive refreshes.

    Search and Replace:
        Find: Users can search for text using the Ctrl+F shortcut, which opens a find dialog that allows case-sensitive and whole-word searching.
        Replace: Users can search and replace text using the Ctrl+H shortcut. There is also an option to replace all occurrences.

    Theme Support:
        Dark Theme: Default theme for the editor with dark background and light text. Syntax highlighting uses soft colors for readability.
        Light Theme: Available as an alternative to the dark theme. Switch between light and dark modes via the "View" menu.
        Dynamic Theme Switching: The syntax highlighter and editor styles adjust dynamically when switching between light and dark themes.

    Customization:
        Change Font: Users can change the font used in the editor via a font dialog, accessible from the "View" menu.

    Text Highlighting and Formatting:
        Current Line Highlighting: The editor highlights the current line where the cursor is placed, making it easier for users to see their active line.
        Auto-Indentation: The editor maintains correct indentation as users type, especially useful for nested HTML/XML elements.
        Bracket/Tag Matching: When typing or navigating through the document, matching opening and closing tags (or brackets) are highlighted automatically.

    Context Menu:
        Snippets Menu: A right-click context menu provides access to HTML snippets that users can quickly insert into their document.
        Standard Actions: The context menu also includes standard actions like undo, redo, copy, paste, etc.

    Live Preview Updates:
        Debounced Preview: The live preview feature updates automatically in real time, with a slight delay (300ms) to avoid performance issues during rapid typing.

Planned/Future Features (Not Yet Fully Implemented or Tested)

    Code Folding: The ability to collapse and expand blocks of code, especially useful for HTML/XML tag structures.
    Bracket Matching (Extended): More advanced bracket or tag matching to ensure correct nesting is visually validated.
    Multi-Caret Editing: An advanced feature that allows editing multiple places simultaneously.
    Error Marking (Planned): Visual error markers for syntax issues in the HTML/XML content.
    Plugin Support (Planned): Support for plugins and extensions to add custom features.
    Integrated Terminal (Planned): An embedded terminal to run commands like npm, git, etc., directly from the editor.
