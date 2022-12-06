odoo.define('tong_hop.phan_bo_chi_phi_tra_truoc_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var PhanBoChiPhiTraTruocController = FormController.extend({
        _onCreate: function () {
            var self = this;

            new dialogs.FormViewDialog(this, {
                readonly: false,
                res_model: 'tong.hop.phan.bo.chi.phi.tra.truoc.tham.so',
                ref_views: [['tong_hop.view_tong_hop_phan_bo_chi_phi_tra_truoc_tham_so_tham_so_form', 'form']],
                title: ("Chọn kỳ phân bổ chi phí"),
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
    
    var PhanBoChiPhiTraTruocView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: PhanBoChiPhiTraTruocController,
        }),
    });
    
    view_registry.add('phan_bo_chi_phi_tra_truoc_view', PhanBoChiPhiTraTruocView);
    
    return PhanBoChiPhiTraTruocView;
});

odoo.define('tong_hop.phan_bo_chi_phi_tra_truoc_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var PhanBoChiPhiTraTruocController = ListController.extend({
        _onCreate: function() {
            var self = this;

            new dialogs.FormViewDialog(this, {
                readonly: false,
                res_model: 'tong.hop.phan.bo.chi.phi.tra.truoc.tham.so',
                ref_views: [['tong_hop.view_tong_hop_phan_bo_chi_phi_tra_truoc_tham_so_tham_so_form', 'form']],
                title: ("Chọn kỳ phân bổ chi phí"),
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
    
    var PhanBoChiPhiTraTruocView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: PhanBoChiPhiTraTruocController,
        }),
    });
    
    view_registry.add('phan_bo_chi_phi_tra_truoc_list_view', PhanBoChiPhiTraTruocView);
    
    return PhanBoChiPhiTraTruocView;
});