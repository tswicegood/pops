if (typeof pops === 'undefined') {
  pops = {};
}

if (typeof pops.inlineFormSet === 'undefined') {
  pops.inlineFormSet = function(opts) {
    var $ = arguments[1] || window.jQuery,
        groupId = '#' + opts.prefix + '-group',
        rows = groupId + ' .tabular.inline-related tbody tr',
        rowsSelector = 'tbody tr:not(.add-row):not(.empty-form)',
        $table = $(rows).closest('table'),
        $totalForms = $table.closest('div.tabular').find('input[id$="TOTAL_FORMS"]'),

        alternatingRows = function(row) {
          $(rows).not('.add-row').removeClass('row1 row2')
            .filter(':even').addClass('row1').end()
            .filter(rows + ':odd').addClass('row2');
        },

        reinitDateTimeShortCuts = function() {
          // TODO: Limit this to effected inputs
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
        },

        deleteLinkForRow = function(row) {
          $(row).find("td.delete a").click(deleteLinkHandler);
        },

        deleteLinkHandler = function() {
          var $this = $(this),
              $row = $this.closest('tr');
          if ($row.is('.has_original')) {
            $this.prev('input').attr('checked', 'checked');
            $row.addClass('deleted_row').fadeTo("fast", 0.5, updatePositions);
            $this.unbind('click', deleteLinkHandler)
              .removeClass('delete')
              .addClass('undo')
              .html(opts.undoHtml)
              .click(undoClickHandler);
          } else {
            $row.fadeTo("fast", 0, function() {
              $row.remove();
              updatePositions();
            });
          }
        },

        updateIdFields = function(row, newPosition) {
          var idExp = /([^ ]+?\-)([0-9]+|__prefix__)(\-[^ ]+)/i;

          $.each(['select', 'input', 'a', 'textarea'], function (i, tagName) {
            row.find(tagName).each(function() {
              var $tag = $(this);
              $.each(['id', 'name'], function (j, attrName) {
                var oldVal = $tag.attr(attrName);
                if (!oldVal) return;
                var newVal = oldVal.replace(idExp, "$1" + newPosition + "$3");
                $tag.attr(attrName, newVal);
              });
            });
          });
        },

        reorderRows = function($rows) {
          if (!opts.positionField) {
            return;
          }

          if (!$rows) {
            $rows = $table.find(rowsSelector);
          }

          $rows.each(function(i) {
            $(this).find('td.' + opts.positionField + ' input').val(i + 1);
          });
        },

        updatePositions = function() {
          var $rows = $table.find(rowsSelector);
          if (opts.positionField) {
            reorderRows($rows);
          }
          $totalForms.val($rows.length);
        },

        undoClickHandler = function() {
          var $this = $(this),
              $row = $this.closest('tr');
          $this.prev('input').removeAttr('checked');
          $row.removeClass('deleted_row').fadeTo('fast', 1.0);
          $this.unbind('click', undoClickHandler)
            .removeClass('undo')
            .addClass('delete')
            .click(deleteLinkHandler)
            .html(opts.deleteHtml);
          updatePositions();
        };

    // Not sure if this is needed?
    $('.tabular-inline textarea').addClass('xxlarge');

    // TODO: Refactor all of these to allow false to turn them off
    if (typeof opts.positionField === 'undefined') {
      opts.positionField = 'order';
    }
    opts.addTextIcon = opts.addTextIcon || '<i class="icon icon-plus"></i> ';
    opts.deleteTextIcon = opts.deleteTextIcon || '<i class="icon icon-minus"></i> ';
    opts.deleteHtml = opts.deleteTextIcon + opts.deleteText;
    opts.emptyCssClass = opts.emptyCssClass || 'empty-form';
    opts.undoTextIcon = opts.undoTextIcon || '<i class="icon icon-undo"></i> ';
    opts.undoText = opts.undoText || 'Undo';
    opts.undoHtml = opts.undoTextIcon + opts.undoText;

    var formsetOptions = {
      prefix: opts.prefix,
      addText: opts.addTextIcon + opts.addText,
      formCssClass: 'dynamic-' + opts.prefix,
      deleteCssClass: 'inline-deletelink btn',
      addCssClass: 'add-row',
      deleteText: opts.deleteHtml,
      emptyCssClass: opts.emptyCssClass,
      removed: alternatingRows,
      added: (function(row) {
        initPrepopulatedFields(row);
        reinitDateTimeShortCuts();
        updateSelectFilter();
        alternatingRows(row);
        reinitChosen(row);
        deleteLinkForRow(row);
        updatePositions();
      })
    };
    $(rows).formset(formsetOptions);

    // once again, go back the jQuery with jQuery UI
    window.jQuery(rows).closest('table').sortable({
      items: 'tbody tr:visible:not(.add-row)',
      tolerance: 'pointer',
      axis: 'y',
      cancel: 'input,button,select,a',
      helper: 'clone',
      update: updatePositions
    });

    // Create all of the delete buttons
    $(rows).not('.' + opts.emptyCssClass).find('td.delete').each(function() {
      var $this = $(this),
          deleteLink = $('<a class="delete btn">' + opts.deleteHtml + '</a>');
      $this.find('input:checkbox').hide();
      deleteLink.click(deleteLinkHandler).css('cursor', 'pointer');
      $this.append(deleteLink);
    });

    $(groupId).find('.add-row a').addClass('btn pull-right');
  };
}
