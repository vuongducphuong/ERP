odoo.define('tong_hop.tinh_ty_gia_xuat_quy_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var TinhTyGiaXuatQuyFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        _onButtonClicked: function(event) {
            var self = this;
            event.stopPropagation();
            switch (event.data.attrs.id)
            {
                case "btn_thuc_hien":
                    var thang = this.getFieldValue('THANG');
                    var nam = this.getFieldValue('NAM');
                    this.rpc_action({
                        model: 'tong.hop.tinh.ty.gia.xuat.quy',
                        method: 'check_ton_tai',
                        args: {
                            'thang' : thang,
                            'nam' : nam,
                        },
                        callback: function(result) {
                            if (result) {
                                if(result[0] == true){
                                    var thong_bao = "Kỳ tính tỷ giá xuất quỹ tháng " + thang + " năm " + nam + " đã có chứng từ xử lý chênh lệch tỷ giá xuất quỹ. \nĐể tính lại tỷ giá xuất quy trong tháng, bạn phải xóa chứng từ trước đi. \nBạn có muốn xem chứng từ đó không";
                                    Dialog.show_message('Thông báo', thong_bao, 'CONFIRM')
                                    .then(function(result_yes_no) {
                                        if(result_yes_no == true){
                                            // new dialogs.FormViewDialog(self, {
                                            //     res_id : result[1].ID_CHUNG_TU,
                                            //     readonly: false,
                                            //     res_model: result[1].MODEL_CHUNG_TU,
                                            //     ref_views: [['tong_hop.view_account_ex_chung_tu_nghiep_vu_khac_form', 'form']],
                                            //     title: 'Xử lý chênh lệch tỷ giá từ tỷ giá xuất quỹ',
                                            //     disable_multiple_selection: true,
                                            //     shouldSaveLocally: false,
                                        
                                            // }).open();

                                            var options = {
                                                res_model: result[1].MODEL_CHUNG_TU,
                                                ref_view: 'tong_hop.view_account_ex_chung_tu_nghiep_vu_khac_form',
                                                res_id:result[1].ID_CHUNG_TU,
                                            }
                                            return self.openFormView(options);
                                        }
                                        
                                    });
                                }
                                else{
                                    self.rpc_action({
                                        model: 'tong.hop.tinh.ty.gia.xuat.quy',
                                        method: 'lay_du_lieu_ty_gia_xuat_quy',
                                        args: {
                                            'thang' : thang,
                                            'nam' : nam,
                                        },
                                        callback: function(result) {
                                            if (result) {
                                                var param_tham_so = result;
                                                if(param_tham_so[2] == false){
                                                    Dialog.show_message('Thông báo', 'Không có phát sinh chênh lệch tỷ giá trong kỳ', 'ALERT')
                                                    .then(function(result) {
                                                        // Xử lý sau khi đóng popup
                                                    });
                                                    return;
                                                }else{
                                                    var options = {
                                                        params : {param_xu_ly_chenh_lech_ty_gia: param_tham_so},
                                                        res_model: 'account.ex.chung.tu.nghiep.vu.khac',
                                                        ref_view: 'tong_hop.view_account_ex_chung_tu_nghiep_vu_khac_form',
                                                    }
                                                    return self.openFormView(options);
                                                }
                                                

                                            }
                                        }
                                    });
                                }
                            }
                        }
                    });
                    break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });

    
    var TinhTyGiaXuatQuyFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TinhTyGiaXuatQuyFormController,
        }),
    });
    
    view_registry.add('tinh_ty_gia_xuat_quy_form_view', TinhTyGiaXuatQuyFormView);
    
    return TinhTyGiaXuatQuyFormView;
});
