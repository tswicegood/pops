if (typeof pops === 'undefined') {
  pops = {};
}

if (typeof pops.inlineFormSet === 'undefined') {
  pops.inlineFormSet = function(opts) {
    var $ = arguments[1] || window.jQuery,
        groupId = '#' + opts.prefix + '-group',
        rows = groupId + ' .tabular.inline-related tbody tr',
        alternatingRows = function(row) {
          $(rows).not('.add-row').removeClass('row1 row2')
            .filter(':even').addClass('row1').end()
            .filter(rows + ':odd').addClass('row2');
        },

        reinitDateTimeShortCuts = function() {
          // Reinitialize the calendar and clock widgets by force
          if (typeof DateTimeShortcuts != 'undefined') {
            $('.datetimeshortcuts').remove();
            DateTimeShortcuts.init();
          }
        },

        reinitChosen = function(row) {
          // Yes, we cheat here since Chosen doesn't know about django.jQuery
          // and window.jQuery doesn't know about django.jQuery.fn.formset
          var $ = window.jQuery;
          $(row).find('.chzn-done').each(function(i, el) {
            $('#' + el.id + '_chzn').remove();
            $(el).removeClass('chzn-done').chosen();
          });
        },

        updateSelectFilter = function() {
          // If any SelectFilter widgets are a part of the new form,
          // instantiate a new SelectFilter instance for it.
          if (typeof SelectFilter != 'undefined'){
            $('.selectfilter').each(function(index, value){
              var namearr = value.name.split('-');
              SelectFilter.init(value.id, namearr[namearr.length-1], false, opt.adminMediaPrefix );
            });
            $('.selectfilterstacked').each(function(index, value){
              var namearr = value.name.split('-');
              SelectFilter.init(value.id, namearr[namearr.length-1], true, opt.adminMediaPrefix );
            });
          }
        },

        initPrepopulatedFields = function(row) {
          row.find('.prepopulated_field').each(function() {
            var field = $(this);
            var input = field.find('input, select, textarea');
            var dependency_list = input.data('dependency_list') || [];
            var dependencies = [];
            $.each(dependency_list, function(i, field_name) {
              dependencies.push('#' + row.find(field_name).find('input, select, textarea').attr('id'));
            });
            if (dependencies.length) {
              input.prepopulate(dependencies, input.attr('maxlength'));
            }
          });
        };

    // Not sure if this is needed?
    $('.tabular-inline textarea').addClass('xxlarge');

    opts.addTextIcon = opts.addTextIcon || '<i class="icon icon-plus"></i> ';
    opts.deleteTextIcon = opts.deleteTextIcon || '<i class="icon icon-minus"></i> ';

    var formsetOptions = {
      prefix: opts.prefix,
      addText: opts.addTextIcon + opts.addText,
      formCssClass: 'dynamic-' + opts.prefix,
      deleteCssClass: 'inline-deletelink btn',
      addCssClass: 'add-row',
      deleteText: opts.deleteTextIcon + opts.deleteText,
      emptyCssClass: 'empty-form',
      removed: alternatingRows,
      added: (function(row) {
        initPrepopulatedFields(row);
        reinitDateTimeShortCuts();
        updateSelectFilter();
        alternatingRows(row);
        reinitChosen(row);

        // double check that it's shown (makes sure this works with dynamic_inlines_with_sorts)
        $(row).show();
      })
    };
    $(rows).formset(formsetOptions);

    $(groupId).find('.add-row a').addClass('btn pull-right');
  };
}
