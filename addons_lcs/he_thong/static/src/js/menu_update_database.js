odoo.define('he_thong.menu_update_database', function (require) {
"use strict";

var core = require('web.core');
var Widget = require('web.Widget');
var Session = require('web.session');
var QWeb = core.qweb;


var KioskMode1 = Widget.extend({
    events: {
        "click #btnGenerate": function(){ 
            var self = this;
            var module = $('#inputModel').val();
            var field = 'company_id';
            var val = 1;
            if (module != '') {
                var def = this._rpc({
                    model: 'ir.model',
                    method: 'update_database',
                    args: [module, field, val]
                })
                .then(function (result) {
                    alert(result);
                });
            }
		},
    },

    start: function () {
        var self = this;
		self.$el.html(QWeb.render("HeThongUpdateDatabase", {widget: self}));
        return this._super.apply(this, arguments);
    },
});

core.action_registry.add('menu_update_database', KioskMode1);

return KioskMode1;

});