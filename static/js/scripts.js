"use strict";

var g_mySwitch;
var g_allOn = true;
var g_pwdOk = false;
var g_reqFieldsOk = false;
var g_submit = ".btn-sit-submit";

$(function() {
    // Define our required handler function. It checks for all required fields on a form.
    // If they are all filled in enable the submit button.
    var reqHandler = function() {
        var fields = $(".sit-required");
        var disable = false;
        for (var i = 0; i < fields.length; i++) { // For loop faster than $.each
            if ($(fields[i]).val() === "") {
                disable = true;
                g_reqFieldsOk = false;
                break;  // No need to go through all the fields.....it just takes one
            }
        }

        if (disable) {
            $(g_submit).addClass("sit-disabled");
        } else {
            g_reqFieldsOk = true; // Holy hell I hate this! ˘L˘
            // If we are on the registration form, we also need to ensure that the
            // password has passed validation/requirements.
            if ($("form").hasClass("register-form")) {
                if (g_pwdOk === true) {
                    $(g_submit).removeClass("sit-disabled");
                }
            } else {
                $(g_submit).removeClass("sit-disabled");
            }        
        }
    };

    // Character count
    var charCountHandler = function() {
        var maxlen = parseInt($(this).attr("maxlength"));
        if (maxlen === "undefined") {return;}
        $(".char-count").text((maxlen - $(this).val().length).toString());
    };

    // Password validation handler. Note: this is minimal validation. I could have
    // used a more sophisticated, already-rolled option, but wanted to do this
    // myself. It gives visual notification that the user has keyed in at least
    // 8 characters and gives visual notification when password and confirm
    // password fields are the same. It does no sort of strength testing/validation
    // whatsoever.
    var pwdHandler = function() {
        if ($("#pwd").val().length >= 8) {
            $("#pwd-ok-icon").removeClass("hide");
            if ($("#pwd").val() === $("#pwd-confirm").val()) {
                $("#pwd-confirm-ok-icon").removeClass("hide");
                g_pwdOk = true;
                // Now check the case where all the other required fields have
                // data and the last thing the user did was enter password information.
                // I really don't like this! ˘L˘ I know there is a better way tos
                // do this, but getting to the end and need to get this submitted.
                if (g_reqFieldsOk) {
                    $(g_submit).removeClass("sit-disabled");
                }
            } else {
                $("#pwd-confirm-ok-icon").addClass("hide");
                g_pwdOk = false;
                if (g_reqFieldsOk) {
                    $(g_submit).addClass("sit-disabled");
                }
            }
        }
        else {
            $("#pwd-ok-icon").addClass("hide");
            $("#pwd-confirm-ok-icon").addClass("hide");
            $(g_submit).addClass("sit-disabled");
            g_pwdOk = false;
        }
    };

    // Call our handler for required field.
    $(document).on("keyup paste", ".sit-required", reqHandler);

    // Call our handler for char countdown fields.
    $(document).on("keyup paste", ".char-countdown", charCountHandler);

    // Call our handler for password verification.
    $(document).on("keyup paste", ".pwd", pwdHandler);

    $(document).on("change keypress keyup paste", ".edit-form", function() {
        {$(g_submit).removeClass("sit-disabled");}
    });

    // Phone validation.....sort of. The only thing this does is prevent
    // the user from entering characters that in no way are part of
    // a phone number. The only acceptable characters are: plus sign,
    // 0-9, left paren, right paren, dash and dot.
    $(document).on("keypress", ".phone-chars-only", function(evt) {
        return /[0-9().-+ ]/.test(evt.key)
    });

    // Post code validation.....sort of. The only thing this does is prevent
    // the user from entering characters that in no way are part of
    // a postcode. The only acceptable characters are: A-Z, 0-9 and a space.
    $(document).on("keypress", ".postcode", function(evt) {
        return /[0-9A-Za-z ]/.test(evt.key)
    });

    // Detect that we are changing the password and bypass required field requirement.
    $("#change-pwd").click(function() {
        g_reqFieldsOk = true;
    });

    // We are not submitting change password form.
    $("#pwd-submit-btn").click(function(evt) {
        evt.preventDefault();
        alert("You must click 'Save' button on profile form to commit password change.")
        $("#pwd-1").val($("#pwd").val());

        // Ha! This is my way of fooling the browser. Given that I am not loading the password
        // into the profile form (I don't believe in needlessly exposing the password, despite being hidden).
        // So, by default the password field is really nothing and of type=text. This way, it 
        // prevents the browser from asking the user if they want to save the password change, when the user
        // is changing other profile information and not the password field. It isn't until they
        // actually bring up the change password modal and save that this becomes a password type field.
        // I suppose another way around this would to not show a field at all and just have only a button
        // to change the password. Hmmm. Maybe slightly over-engineered. ˘L˘
        $("#pwd-1").attr("type", "password");

        $("#change-pwd-modal").modal("hide");
        
        // Be on the safe side and clear when not needed.
        $("#pwd").val("");
        $("#pwd-confirm").val("");

        // Tell the back end that we changed the password
        $("#pwd-changed").val("1");        
    });

    // Change the caret widget and popup text dynamically
    // .data() method does not work consistently here -- need to use .attr() 
    $('.show-hide-detail').click(function() {
        var title = $(this).attr("data-original-title");
        var altTitle = $(this).attr("data-title-alt");

        $(this).tooltip("hide")
                .attr("data-original-title", altTitle)
                .attr("data-title-alt", title);

        if ($(this).hasClass('toggle-caret')) {
            $(`#caret-widget-${$(this).attr("data-id")}`).toggleClass("cta-icon view-details fa fa-caret-right");
            $(`#caret-widget-${$(this).attr("data-id")}`).toggleClass("cta-icon hide-details fa fa-caret-down");
        }

        $(this).tooltip("show")
    });

    // Expand or collapse the correct issue or feature detail section
    $(".detail-toggle").click(function() {
        var idOfCollapse = $(this).attr("href");
        if ($(idOfCollapse).is(":hidden")) {
            var altText = $(this).attr("data-alt-text");
            $(this).attr("data-alt-text", $(this).text());
            $(this).text(altText);
            $(this).addClass("open");
        } else if ($(idOfCollapse).is(":visible")) {
            var altText = $(this).attr("data-alt-text");
            $(this).attr("data-alt-text", $(this).text());
            $(this).text(altText);
            $(this).removeClass("open");
        }
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
            $("button.cat-filter-toggle").each(function(idx) {
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
            $("button.iss-status-filter-toggle").each(function(idx) {
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
