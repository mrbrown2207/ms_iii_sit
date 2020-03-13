"use strict";

$(function() {
    // Define our required handler function. It checks for all required fields on a form.
    // If they are all filled in enable the submit button.
    var reqHandler = function() {
        var fields = $(".sit-required");
        var disable = false;
        for (var i = 0; i < fields.length; i++) { // For loop faster than $.each
            if ($(fields[i]).val() === "") {
                disable = true;
                break;  // No need to go through all the fields.....it just takes one
            }
        }

        if (disable) {$("#submit-btn").addClass("sit-disabled");}
        else {$("#submit-btn").removeClass("sit-disabled");}
    };

    // Character count
    var charCountHandler = function() {
        var maxlen = parseInt($(this).attr("maxlength"));
        if (maxlen === "undefined") {return;}
        $(".char-count").text((maxlen - $(this).val().length).toString());
    };

    // Call our handler for required field.
    $(document).on("keyup paste", ".sit-required", reqHandler);

    // Call our handler for char countdown fields.
    $(document).on("keyup paste", ".char-countdown", charCountHandler);

    // Any changes to the profile form enable the submit button.
    $(document).on("keyup paste", "#profile-form", function() {
        $("#submit-btn").removeClass("sit-disabled");
    });

    // Change the caret widget and popup text dynamically
    $('.toggle-caret').click(function() {
        var title = $(this).attr("data-original-title");
        var altTitle = $(this).attr("data-title-alt");

        $(this).tooltip("hide")
                .attr("data-original-title", altTitle)
                .attr("data-title-alt", title);

        $(`#caret-widget-${$(this).attr("data-id")}`).toggleClass("cta-icon view-details fa fa-caret-right");
        $(`#caret-widget-${$(this).attr("data-id")}`).toggleClass("cta-icon hide-details fa fa-caret-down");

        $(this).tooltip("show")
    });

    // Bootstrap tooltip
    $('[data-toggle-1="tooltip"]').tooltip();

    // Numeric or alpha only field checking
    $(document).on("keypress paste", ".numeric-only", function(key) {
        if (key.charCode < 48 || key.charCode > 57) {return false;}
    });
    $(document).on("keypress paste", ".alpha-only", function(key) {
        if (key.charCode >= 48 && key.charCode <= 57) {return false;}
    });

    // For small form factor devices. Filters become a popover dropdown menu
    $('[data-toggle="filter-popover-issues"]').popover( {
        html: true,
        content: function() {
            return $('#filter-popover-menu-issues').html();
        }
    });
    $('[data-toggle="filter-popover-features"]').popover( {
        html: true,
        content: function() {
            return $('#filter-popover-menu-features').html();
        }
    });
});
