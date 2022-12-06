odoo.define('asset.tinh_khau_hao_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var AssetTinhKhauHaoController = FormController.extend({
        _onCreate: function () {
            var self = this;
            // new dialogs.FormParamsDialog(this, _.extend({}, this.nodeOptions, {
            //     res_model: 'asset.chon.ky.tinh.khau.hao',
            //     title: 'Tính khấu hao',
            //     ref_views: [['asset.view_asset_chon_ky_tinh_khau_hao_tham_so_form', 'form']],
            //     on_selected: function (params) {
            //         var context = {'default_THANG': params.THANG,
            //                        'default_THANG': params.NAM,
            //                     }
            //         self.createRecord(context);
            //     },
            // })).open();

            new dialogs.FormViewDialog(this, {
                readonly: false,
                res_model: 'asset.chon.ky.tinh.khau.hao',
                ref_views: [['asset.view_asset_chon_ky_tinh_khau_hao_tham_so_form', 'form']],
                title: ("Tính khấu hao"),
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
    
    var AssetTinhKhauHaoView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: AssetTinhKhauHaoController,
        }),
    });
    
    view_registry.add('tinh_khau_hao_form_view', AssetTinhKhauHaoView);
    
    return AssetTinhKhauHaoView;
});

odoo.define('asset.tinh_khau_hao_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var AssetTinhKhauHaoController = ListController.extend({
        _onCreate: function() {
            var self = this;
            // new dialogs.FormParamsDialog(this, _.extend({}, this.nodeOptions, {
            //     res_model: 'asset.chon.ky.tinh.khau.hao',
            //     title: 'Tính khấu hao',
            //     ref_views: [['asset.view_asset_chon_ky_tinh_khau_hao_tham_so_form', 'form']],
            //     on_selected: function (params) {
            //         var context = {'default_THANG': params.THANG,
            //                        'default_THANG': params.NAM,
            //                     }
            //         self.createRecord(context);
            //     },
            // })).open();

            new dialogs.FormViewDialog(this, {
                readonly: false,
                res_model: 'asset.chon.ky.tinh.khau.hao',
                ref_views: [['asset.view_asset_chon_ky_tinh_khau_hao_tham_so_form', 'form']],
                title: ("Tính khấu hao"),
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
    
    var AssetTinhKhauHaoView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: AssetTinhKhauHaoController,
        }),
    });
    
    view_registry.add('tinh_khau_hao_list_view', AssetTinhKhauHaoView);
    
    return AssetTinhKhauHaoView;
});