odoo.define('purchase_ex.purchase_ex_nhan_hoa_don_mua_hang_hoa_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var HoaDonMuaHangController = FormController.extend({
        _onCreate: function () {
            var self = this;
            new dialogs.FormViewDialog(this, {
                readonly: false,
                res_model: 'purchase.ex.nhan.hoa.don',
                ref_views: [['purchase_ex.view_purchase_ex_nhan_hoa_don_tham_so_form', 'form']],
                title: 'Chọn chứng từ mua hàng hóa cần nhận hóa đơn',
//                 size : 'medium',
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
    
    var HoaDonMuaHangView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: HoaDonMuaHangController,
        }),
    });
    
    view_registry.add('purchase_ex_nhan_hoa_don_mua_hang_hoa_form_view', HoaDonMuaHangView);
    
    return HoaDonMuaHangView;
});

odoo.define('purchase_ex.purchase_ex_nhan_hoa_don_mua_hang_hoa_form_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var HoaDonMuaHangController = ListController.extend({
        _onCreate: function() {
            var self = this;
            new dialogs.FormViewDialog(this, {
                readonly: false,
                res_model: 'purchase.ex.nhan.hoa.don',
                ref_views: [['purchase_ex.view_purchase_ex_nhan_hoa_don_tham_so_form', 'form']],
                title: 'Chọn chứng từ mua hàng hóa cần nhận hóa đơn',
//                 size : 'medium',
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
    
    var HoaDonMuaHangView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: HoaDonMuaHangController,
        }),
    });
    
    view_registry.add('purchase_ex_nhan_hoa_don_mua_hang_hoa_form_list_view', HoaDonMuaHangView);
    
    return HoaDonMuaHangView;
});