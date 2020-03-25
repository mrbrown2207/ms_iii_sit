"use strict";

var g_mySwitch;
var g_allOn = true;

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
    // .data() method does not work consistently here -- need to use .attr() 
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

    // Set current id and subject for display in modal when resolving issue
    $(".resolve-iss").click(function() {
        $("#curr-iss-id").val($(this).data("iss-id"))
        $("#curr-iss-subj").val($(this).data("iss-subj"))
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

    $(document).on("change keypress paste", ".edit-form", function() {
        {$("#submit-btn").removeClass("sit-disabled");}
    });

    // Filter categories toggle control. Note that the all-cat-filters can only
    // be toggled on, it cannot be toggled off. This code ensures
    // that everything is in the right state.
    $("#all-cats-toggle").click(function(evt) {
        evt.preventDefault();
        $(this)
            .removeClass("filter-not-selected")
            .addClass("filter-selected");

        $(".cat-filter-toggle")
            .val("1")
            .removeClass("filter-not-selected")
            .addClass("filter-selected");
    });

    $(".cat-filter-toggle").click(function(evt) {
        evt.preventDefault();
        if ($(this).val() === "1") {
            // Let's check and ensure this isn't the last filter that is enabled.
            let x = 0;
            $(".cat-filter-toggle").each(function(idx) {
                x += parseInt($(this).val());
            });
            if (x === 1) {
                alert("You must have at least one category filter selected.");
                return false;
            }

            // Here we change the button value and the next element. The next
            // element needs to be the input field that we will pass back to
            // the server when submitting the form. We only bother with changing the
            // button value for consistency. And interestingly, .next().val("blah")
            // would not work ˘L˘
            $(this).val("0").next().attr("value", "0");
        } else {
            $(this).val("1").next().attr("value", "1");
        }

        $(this).toggleClass("filter-selected").toggleClass("filter-not-selected");

        let x = false;
        $(".cat-filter-toggle").each(function(idx) {
            if ($(this).val() === "0") {x = true;}
        });

        if (x) {
            $("#all-cats-toggle")
                .removeClass("filter-selected")
                .addClass("filter-not-selected");
        } else {
            $("#all-cats-toggle")
                .removeClass("filter-not-selected")
                .addClass("filter-selected");
        }
    });

    // Filter issue status toggle control. Note that the all-cat-filters can only
    // be toggled on, it cannot be toggled off. This code ensures that everything 
    // is in the right state.
    $("#all-iss-status-toggle").click(function(evt) {
        evt.preventDefault();
        $(this)
            .removeClass("filter-not-selected")
            .addClass("filter-selected");

        $(".iss-status-filter-toggle")
            .val("1")
            .removeClass("filter-not-selected")
            .addClass("filter-selected");
    });

    $(".iss-status-filter-toggle").click(function(evt) {
        evt.preventDefault();
        if ($(this).val() === "1") {
            // Let's check and ensure this isn't the last filter that is enabled.
            let x = 0;
            $(".iss-status-filter-toggle").each(function(idx) {
                x += parseInt($(this).val());
            });
            if (x === 1) {
                alert("You must have at least one issue status filter selected.");
                return false;
            }

            // Here we change the button value and the next element. The next
            // element needs to be the input field that we will pass back to
            // the server when submitting the form. We only bother with changing the
            // button value for consistency. And interestingly, .next().val("blah")
            // would not work ˘L˘
            $(this).val("0").next().attr("value", "0");
        } else {
            $(this).val("1").next().attr("value", "1");
        }

        $(this).toggleClass("filter-selected").toggleClass("filter-not-selected");

        let x = false;
        $(".iss-status-filter-toggle").each(function(idx) {
            if ($(this).val() === "0") {x = true;}
        });

        if (x) {
            $("#all-iss-status-toggle")
                .removeClass("filter-selected")
                .addClass("filter-not-selected");
        } else {
            $("#all-iss-status-toggle")
                .removeClass("filter-not-selected")
                .addClass("filter-selected");
        }
    });
});
