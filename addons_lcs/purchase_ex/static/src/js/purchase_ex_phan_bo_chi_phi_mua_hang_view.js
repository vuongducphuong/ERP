odoo.define('purchase_ex.phan_bo_chi_phi_mua_hang_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');


    var PhanBoChiPhiMuaHangController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        onViewLoaded: function(e, defer) {
            var self = this;
            var def = defer;
            var du_lieu = self.params.tham_so;
            self.changeFieldValue('PHUONG_THUC_PHAN_BO', 'TY_LE_PT_THEO_SO_LUONG');
            self.changeFieldValue('TONG_TIEN_HANG', du_lieu[0]);
            self.updateUI({'PHAN_BO_CHI_PHI_MUA_HANG_IDS': du_lieu[1]});
            self.changeFieldValue('TONG_CHI_PHI_MUA_HANG', du_lieu[2]);
            //var fieldWidget = this.getFieldWidget('PHAN_BO_CHI_PHI_MUA_HANG_IDS');
            // fieldWidget.do_active_column('TY_LE_PHAN_BO',true);
            // fieldWidget.do_active_column('CHI_PHI_MUA_HANG',true);
            def.resolve();
        },

        //onFieldChanged: function(field){
        //    var self =this;
        //    if("PHUONG_THUC_PHAN_BO" == field){
        //        var phuong_thuc_phan_bo = this.getFieldValue('PHUONG_THUC_PHAN_BO');
        //        if(phuong_thuc_phan_bo == false){
        //            Dialog.show_message('', 'Bạn phải chọn phương thức thanh toán', 'ALERT')
        //            .then(function(result) {
        //                // Xử lý sau khi đóng popup
        //                return;
        //            });
        //        } else if(phuong_thuc_phan_bo == 'TU_NHAP_PT'){
        //            var fieldWidget = this.getFieldWidget('PHAN_BO_CHI_PHI_MUA_HANG_IDS');
        //            // fieldWidget.do_active_column('TY_LE_PHAN_BO',false);
        //        } else if(phuong_thuc_phan_bo == 'TU_NHAP_GIA_TRI'){
        //            var fieldWidget = this.getFieldWidget('PHAN_BO_CHI_PHI_MUA_HANG_IDS');
        //            // fieldWidget.do_active_column('CHI_PHI_MUA_HANG',false);
        //        }

        //    }
        //},

        _onButtonClicked: function(event) {
            var self = this;
            event.stopPropagation();
            var def = $.Deferred();
            var error = [];
            switch (event.data.attrs.id)
            {
                
                case "btn_phan_bo":
//                     var current_data = event.data.record.data;
                    // Lấy data của chứng từ chi tiết
                    var phuong_thuc_phan_bo = this.getFieldValue('PHUONG_THUC_PHAN_BO');
                    var tong_thanh_tien = this.getFieldValue('TONG_TIEN_HANG');
                    var chi_tiet = this.getFieldValue('PHAN_BO_CHI_PHI_MUA_HANG_IDS');
                    var tong_chi_phi_mua_hang = this.getFieldValue('TONG_CHI_PHI_MUA_HANG');

                    if(phuong_thuc_phan_bo == null){
                        error = 'Bạn phải chọn phương thức phân bổ';
                    }
                    if (error.length) {
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                        return def;
                    } else {
                        def.resolve(true);
                    }
                    this.rpc_action({
                        model: 'purchase.document',
                        method: 'chung_tu_phan_bo_chi_phi_mua_hang',
                        args: {
                            'phuong_thuc_phan_bo' : phuong_thuc_phan_bo,
                            'chi_tiet' : chi_tiet,
                            'tong_chi_phi_mua_hang' : tong_chi_phi_mua_hang,
                            'tong_thanh_tien' : tong_thanh_tien,
                        },
                        callback: function(result) {
                            if (result) {
//                                 var tong_chi_phi_mua_hang_sau_pb = 0;
//                                 for(var i in result){
//                                     tong_chi_phi_mua_hang_sau_pb += result[i].CHI_PHI_MUA_HANG;
//                                 }
//                                 if(tong_chi_phi_mua_hang_sau_pb != tong_chi_phi_mua_hang){
//                                     Dialog.show_message('', 'Tổng <Chi phí mua hàng> phân bổ cho các mặt hàng phải bằng <Tổng chi phí mua hàng>', 'ALERT')
//                                     .then(function(result) {
//                                         // Xử lý sau khi đóng popup
//                                     });

//                                 }
                                self.updateUI({'PHAN_BO_CHI_PHI_MUA_HANG_IDS': result});
                            }
                        }
                    });
                    
                    break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });
    
    var PhanBoChiPhiMuaHangView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: PhanBoChiPhiMuaHangController,
        }),
    });
    
    view_registry.add('phan_bo_chi_phi_mua_hang_view', PhanBoChiPhiMuaHangView);
    
    return PhanBoChiPhiMuaHangView;
});
