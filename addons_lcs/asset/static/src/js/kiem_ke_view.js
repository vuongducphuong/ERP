odoo.define('asset.kiem_ke_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var AssetKiemKeController = FormController.extend({
        _onCreate: function () {
            var self = this;

            new dialogs.FormViewDialog(this, {
                readonly: false,
                res_model: 'asset.kiem.ke.tham.so',
                ref_views: [['asset.view_asset_kiem_ke_tham_so_tham_so_form', 'form']],
                title: ("Kiểm kê tài sản cố định"),
                disable_multiple_selection: true,
                size : 'medium',
                shouldSaveLocally: true,
                // on_saved: function (record, changed) {
                        //     if (changed) {
                        //         self.cReload();
                        //     }
                        // },
            }).open();
        },

        
    });
    
    var AssetKiemKeView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: AssetKiemKeController,
        }),
    });
    
    view_registry.add('kiem_ke_form_view', AssetKiemKeView);
    
    return AssetKiemKeView;
});

odoo.define('asset.kiem_ke_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var AssetKiemKeController = ListController.extend({
        _onCreate: function() {
            var self = this;

            new dialogs.FormViewDialog(this, {
                readonly: false,
                res_model: 'asset.kiem.ke.tham.so',
                ref_views: [['asset.view_asset_kiem_ke_tham_so_tham_so_form', 'form']],
                title: ("Kiểm kê tài sản cố định"),
                disable_multiple_selection: true,
                size : 'medium',
                shouldSaveLocally: true,
                // on_saved: function (record, changed) {
                        //     if (changed) {
                        //         self.cReload();
                        //     }
                        // },
            }).open();
            
        },
    });
    
    var AssetKiemKeView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: AssetKiemKeController,
        }),
    });
    
    view_registry.add('kiem_ke_list_view', AssetKiemKeView);
    
    return AssetKiemKeView;
});