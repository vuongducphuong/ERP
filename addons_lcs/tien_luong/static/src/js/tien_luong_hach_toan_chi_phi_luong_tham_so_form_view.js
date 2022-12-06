odoo.define('tien_luong.tien_luong_hach_toan_chi_phi_luong_tham_so_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');
   
    var TienLuongHachToanChiPhiLuongFormThamSoController = FormController.extend({
        on_before_saved: function() {
            var def = $.Deferred();
            var self = this;
            var error = [];
            var bang_luong_id;
            var bang_luong = self.getFieldValue('BANG_LUONG');
            if (bang_luong){
                bang_luong_id = bang_luong.id;
            }
            self.rpc_action({
                model: 'tien.luong.hach.toan.chi.phi.luong.form.tham.so',
                method: 'kiem_tra_bang_luong_ton_tai',
                args: {
                    'bang_luong_id' : bang_luong_id,
                },
                callback: function(result) {
                    if (result ==true) {
                        error = 'Đã tồn tại chứng từ hạch toán chi phí với bảng lương này, vui lòng chọn bảng lương khác để thực hiện kết chuyển.';
                    }
                    if (error.length) {
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                    } else {
                        def.resolve(true);
                    }
                       
                }
                });
                return def; 
                
        },
    });
    
    var TienLuongHachToanChiPhiLuongFormThamSoView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TienLuongHachToanChiPhiLuongFormThamSoController,
        }),
    });
    
    view_registry.add('tien_luong_hach_toan_chi_phi_luong_tham_so_form_view', TienLuongHachToanChiPhiLuongFormThamSoView);
    
    return TienLuongHachToanChiPhiLuongFormThamSoView;
});
