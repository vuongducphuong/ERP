odoo.define('supply.phan_bo_chi_phi_fom_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var SupplyPhanBoChiPhiController = FormController.extend({
        _onCreate: function () {
            var self = this;
            new dialogs.FormViewDialog(this, {
                // tham_so : dict_param,
                readonly: false,
                res_model: 'supply.phan.bo.chi.phi.tham.so',
                ref_views: [['supply.view_supply_phan_bo_chi_phi_tham_so_tham_so_form', 'form']],
                title: ("Chọn kỳ tính chi phí CCDC"),
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
    
    var SupplyPhanBoChiPhiView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: SupplyPhanBoChiPhiController,
        }),
    });
    
    view_registry.add('phan_bo_chi_phi_fom_view', SupplyPhanBoChiPhiView);
    
    return SupplyPhanBoChiPhiView;
});

odoo.define('supply.phan_bo_chi_phi_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var SupplyPhanBoChiPhiController = ListController.extend({
        _onCreate: function() {
            var self = this;
            // new dialogs.FormParamsDialog(this, _.extend({}, this.nodeOptions, {
            //     res_model: 'supply.phan.bo.chi.phi.tham.so',
            //     title: 'Chọn kỳ tính chi phí CCDC',
            //     size : small ,
            //     ref_views: [['supply.view_supply_phan_bo_chi_phi_tham_so_tham_so_form', 'form']],
            //     on_selected: function (params) {
            //         // var context = {'default_THANG': params.THANG,
            //         //                'default_THANG': params.NAM,
            //         //             }
            //         // self.createRecord(context);
            //     },
            // })).open();

            new dialogs.FormViewDialog(this, {
                // tham_so : dict_param,
                readonly: false,
                res_model: 'supply.phan.bo.chi.phi.tham.so',
                ref_views: [['supply.view_supply_phan_bo_chi_phi_tham_so_tham_so_form', 'form']],
                title: ("Chọn kỳ tính chi phí CCDC"),
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
    
    var SupplyPhanBoChiPhiView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: SupplyPhanBoChiPhiController,
        }),
    });
    
    view_registry.add('phan_bo_chi_phi_list_view', SupplyPhanBoChiPhiView);
    
    return SupplyPhanBoChiPhiView;
});