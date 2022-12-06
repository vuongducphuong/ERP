odoo.define('supply.supply_kiem_ke_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var SupplyKiemKeController = FormController.extend({
        _onCreate: function () {
            var self = this;
            new dialogs.FormViewDialog(this, {
                readonly: false,
                res_model: 'supply.kiem.ke.tham.so',
                ref_views: [['supply.view_supply_kiem_ke_tham_so_tham_so_form', 'form']],
                title: ("Kiểm kê CCDC"),
                size : 'medium',
                disable_multiple_selection: true,
                shouldSaveLocally: true,
                // on_saved: function (record, changed) {
                        //     if (changed) {
                        //         self.cReload();
                        //     }
                        // },
            }).open();
        },
    });
    
    var SupplyKiemKeView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: SupplyKiemKeController,
        }),
    });
    
    view_registry.add('supply_kiem_ke_form_view', SupplyKiemKeView);
    
    return SupplyKiemKeView;
});

odoo.define('supply.supply_kiem_ke_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var SupplyKiemKeController = ListController.extend({
        _onCreate: function() {
            var self = this;

            new dialogs.FormViewDialog(this, {
                readonly: false,
                res_model: 'supply.kiem.ke.tham.so',
                ref_views: [['supply.view_supply_kiem_ke_tham_so_tham_so_form', 'form']],
                title: ("Kiểm kê CCDC"),
                size : 'medium',
                disable_multiple_selection: true,
                shouldSaveLocally: true,
                // on_saved: function (record, changed) {
                        //     if (changed) {
                        //         self.cReload();
                        //     }
                        // },
            }).open();
            
        },
    });
    
    var SupplyKiemKeView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: SupplyKiemKeController,
        }),
    });
    
    view_registry.add('supply_kiem_ke_list_view', SupplyKiemKeView);
    
    return SupplyKiemKeView;
});