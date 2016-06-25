var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.getSession().setMode("ace/mode/python");
editor.setOptions({
    fontFamily: "Inconsolata, Monaco, Monospace",
    fontSize: "10pt"
});
