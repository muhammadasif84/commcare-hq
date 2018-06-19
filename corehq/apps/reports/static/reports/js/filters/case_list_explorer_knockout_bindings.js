hqDefine("reports/js/filters/case_list_explorer_knockout_bindings", ['jquery', 'knockout', 'hqwebapp/js/atwho', 'ace-builds/src-min-noconflict/ace'], function($, ko, atwho) {

    ko.bindingHandlers.xPathAutocomplete = {
        init: function(element, valueAccessor, allBindings, viewModel, bindingContext) {
            var $element = $(element),
                editor = ace.edit(
                    element,
                    {
                        enableLiveAutocompletion: true,
                        showPrintMargin: false,
                        showLineNumbers: false,
                        showFoldWidgets: false,
                        showGutter: false,
                        highlightGutterLine: false,
                        highlightActiveLine: false,
                        maxLines: 30,
                        minLines: 3,
                        fontSize: 14,
                        wrap: true,
                        useWorker: false, // enable the worker to show syntax errors
                    }
                );
            editor.session.setMode('ace/mode/xquery'); // does reasonable syntax highlighting for XPath
            editor.on('change', function(){
                viewModel.query(editor.getValue());
                $element.parent().trigger('change');
            });

            // Set placeholder
            function update() {
                // https://stackoverflow.com/a/26700324/2957657
                var shouldShow = !editor.session.getValue().length,
                    node = editor.renderer.emptyMessageNode;
                if (!shouldShow && node) {
                    editor.renderer.scroller.removeChild(editor.renderer.emptyMessageNode);
                    editor.renderer.emptyMessageNode = null;
                } else if (shouldShow && !node) {
                    node = editor.renderer.emptyMessageNode = document.createElement("div");
                    node.textContent = gettext("e.g. (dob <= '2017-02-01' and initial_home_visit_completed = 'yes') ");
                    node.className = "ace_invisible ace_emptyMessage";
                    node.style.padding = "0 9px";
                    editor.renderer.scroller.appendChild(node);
                }
            }
            editor.on("input", update);
            setTimeout(update, 100);
        },
        update: function(element, valueAccessor){
            var casePropertyAutocomplete = {
                getCompletions: function(editor, session, pos, prefix, callback){
                    var data = ko.utils.unwrapObservable(valueAccessor());
                    callback(null, _.map(data, function(suggestion){
                        return {name: suggestion.name, value: suggestion.name, meta: suggestion.case_type || suggestion.meta_type};
                    }));
                }
            };
            ace.require("ace/ext/language_tools").setCompleters([casePropertyAutocomplete]);
        }
    };

    ko.bindingHandlers.explorerColumnsAutocomplete = {
        init: function(element) {
            var $element = $(element);
            if (!$element.atwho) {
                throw new Error("The typeahead binding requires Atwho.js and Caret.js");
            }

            atwho.init($element, {
                atwhoOptions: {
                    displayTpl: function(item){
                        if (item.case_type){
                            return '<li><span class="label label-default">${case_type}</span> ${name}</li>';
                        }
                        return '<li><span class="label label-primary">${meta_type}</span> ${name}</li>';
                    },
                },
                afterInsert: function() {
                    $element.trigger('textchange');
                },
            });

            $element.on("textchange", function() {
                if ($element.val()) {
                    $element.change();
                }
            });
        },

        update: function(element, valueAccessor) {
            $(element).atwho('load', '', ko.utils.unwrapObservable(valueAccessor()));
        },
    };

    return {
        xPathAutocomplete: ko.bindingHandlers.xPathAutocomplete,
        explorerColumnsAutocomplete: ko.bindingHandlers.explorerColumnsAutocomplete,
    };
});
