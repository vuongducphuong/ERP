odoo.define('gia_thanh.ket_chuyen_chi_phi_cong_trinh_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var KetChuyenChiPhiCongTrinhFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        _onCreate: function() {
            var self = this;
            var domain_san_xuat_lien_tuc_gian_don ='CONG_TRINH';
            new dialogs.FormViewDialog(this, {
                tham_so:domain_san_xuat_lien_tuc_gian_don,
                readonly: false,
                res_model: 'gia.thanh.chon.ky.tinh.gia.thanh.ket.chuyen.form',
                ref_views: [['gia_thanh.view_gia_thanh_chon_ky_tinh_gia_thanh_ket_chuyen_form_tham_so_form', 'form']],
                title: ("Chọn kỳ tính giá thành"),
                disable_multiple_selection: true,
                size : 'medium',
                shouldSaveLocally: true,
                on_before_saved: function(controller) {
                    var def = $.Deferred();
                    var isDef = false;
                    var error = [];
                    var ky_tinh_gia_thanh_id = controller.getFieldValue('KY_TINH_GIA_THANH_ID').id;
                    controller.rpc_action({
                        model: 'gia.thanh.chon.ky.tinh.gia.thanh.ket.chuyen.form',
                        method: 'kiem_tra_ket_chuyen_chi_phi',
                        args: {
                            'ky_tinh_gia_thanh_id' : ky_tinh_gia_thanh_id,
                        },
                        callback: function(result) {
                            if (result != 0) {
                                Dialog.show_message('', 'Đã tồn tại chứng từ kết chuyển chi phí của kỳ tính giá thành này. Bạn có muốn xem chứng từ này không?', 'CONFIRM')
                                .then(function(result_yes_no) {
                                    if (result_yes_no == true){
                                        new dialogs.FormViewDialog(self, {
                                            res_id : result,
                                            readonly: false,
                                            res_model: 'gia.thanh.ket.chuyen.chi.phi',
                                            ref_views: [['gia_thanh.view_gia_thanh_ket_chuyen_chi_phi_cong_trinh_form', 'form']],
                                            title: 'Kết chuyển chi phí',
                                            disable_multiple_selection: true,
                                            shouldSaveLocally: false,
                                    
                                        }).open();
                                    }
                                    def.resolve(false);
                                });
                    
                        
                            } else{
                                def.resolve(true);
                            }             
                    }});
                    return def;   
                },
                on_after_saved: function (record, changed) {
                    if (changed) {
                        var ky_tinh_gia_thanh = record.data.KY_TINH_GIA_THANH_ID.data.display_name;
                        var ky_tinh_gia_thanh_id = record.data.KY_TINH_GIA_THANH_ID.data.id;
                        var ngay_hach_toan = record.data.DEN_NGAY
                        var context = {
                            'default_KY_TINH_GIA_THANH': ky_tinh_gia_thanh,
                            'default_KY_TINH_GIA_THANH_ID': ky_tinh_gia_thanh_id,
                            'default_NGAY_HACH_TOAN': ngay_hach_toan,
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
            
        },
        onViewLoaded: function(e, defer) {
            var self = this;
            var def =  defer;
			if (self.params && self.params.tham_so){                
                self.updateUI({'KY_TINH_GIA_THANH':self.params.tham_so['ten'],
                'LOAI_CHUNG_TU':self.params.tham_so['loai_chung_tu'],
                });
            }
            if(self.params && self.params.form_them_moi == true){
                this.rpc_action({
                    model: 'gia.thanh.ket.chuyen.chi.phi',
                    method: 'lay_du_lieu_ket_chuyen_cp_he_so_ty_le',
                    args: {'ky_tinh_gia_thanh_id' : self.params.ky_tinh_gia_thanh_id},
                    callback: function(result) {
                        if (result) {
                            self.updateUI(result);
                        }

                    }
                });
            }
            def.resolve();
        },
        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {
                case "btn_duyet":
                    new dialogs.FormViewDialog(this, {
                        // tham_so : dict_param,
                        readonly: false,
                        res_model: 'gia.thanh.danh.sach.ket.chuyen.chi.phi',
                        ref_views: [['gia_thanh.view_gia_thanh_danh_sach_ket_chuyen_chi_phi_tham_so_form', 'form']],
                        title: ("Danh sách kết chuyển chi phí"),
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        // on_saved: function (record, changed) {
                                //     if (changed) {
                                //         self.cReload();
                                //     }
                                // },
                    }).open();
                    break;
                default: 
                   this._super.apply(this, arguments);
            }
            
        },
    });
    
    var KetChuyenChiPhiCongTrinhFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
           
            Controller: KetChuyenChiPhiCongTrinhFormController,
        }),
    });
    
    view_registry.add('ket_chuyen_chi_phi_cong_trinh_form_view', KetChuyenChiPhiCongTrinhFormView);
    
    return KetChuyenChiPhiCongTrinhFormView;
});
odoo.define('gia_thanh.ket_chuyen_chi_phi_cong_trinh_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var KetChuyenChiPhiCongTrinhController = ListController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        _onCreate: function() {
            var self = this;
            var domain_san_xuat_lien_tuc_gian_don ='CONG_TRINH';
            new dialogs.FormViewDialog(this, {
                tham_so:domain_san_xuat_lien_tuc_gian_don,
                readonly: false,
                res_model: 'gia.thanh.chon.ky.tinh.gia.thanh.ket.chuyen.form',
                ref_views: [['gia_thanh.view_gia_thanh_chon_ky_tinh_gia_thanh_ket_chuyen_form_tham_so_form', 'form']],
                title: ("Chọn kỳ tính giá thành"),
                disable_multiple_selection: true,
                size : 'medium',
                shouldSaveLocally: true,
                on_before_saved: function(controller) {
                    var def = $.Deferred();
                    var isDef = false;
                    var error = [];
                    var ky_tinh_gia_thanh_id = controller.getFieldValue('KY_TINH_GIA_THANH_ID').id;
                    controller.rpc_action({
                        model: 'gia.thanh.chon.ky.tinh.gia.thanh.ket.chuyen.form',
                        method: 'kiem_tra_ket_chuyen_chi_phi',
                        args: {
                            'ky_tinh_gia_thanh_id' : ky_tinh_gia_thanh_id,
                        },
                        callback: function(result) {
                            if (result != 0) {
                                Dialog.show_message('', 'Đã tồn tại chứng từ kết chuyển chi phí của kỳ tính giá thành này. Bạn có muốn xem chứng từ này không?', 'CONFIRM')
                                .then(function(result_yes_no) {
                                    if (result_yes_no == true){
                                        new dialogs.FormViewDialog(self, {
                                            res_id : result,
                                            readonly: false,
                                            res_model: 'gia.thanh.ket.chuyen.chi.phi',
                                            ref_views: [['gia_thanh.view_gia_thanh_ket_chuyen_chi_phi_cong_trinh_form', 'form']],
                                            title: 'Kết chuyển chi phí',
                                            disable_multiple_selection: true,
                                            shouldSaveLocally: false,
                                    
                                        }).open();
                                    }
                                    def.resolve(false);
                                });
                    
                        
                            } else{
                                def.resolve(true);
                            }             
                    }});
                    return def;   
                },
                on_after_saved: function (record, changed) {
                    if (changed) {
                        var ky_tinh_gia_thanh = record.data.KY_TINH_GIA_THANH_ID.data.display_name;
                        var ky_tinh_gia_thanh_id = record.data.KY_TINH_GIA_THANH_ID.data.id;
                        var ngay_hach_toan = record.data.DEN_NGAY
                        var context = {
                            'default_KY_TINH_GIA_THANH': ky_tinh_gia_thanh,
                            'default_KY_TINH_GIA_THANH_ID': ky_tinh_gia_thanh_id,
                            'default_NGAY_HACH_TOAN': ngay_hach_toan,
                            'form_them_moi' : true,
                            'ky_tinh_gia_thanh_id' : ky_tinh_gia_thanh_id,
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
            
        },
    });
    
    var KetChuyenChiPhiCongTrinhView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: KetChuyenChiPhiCongTrinhController,
        }),
    });
    
    view_registry.add('ket_chuyen_chi_phi_cong_trinh_list_view', KetChuyenChiPhiCongTrinhView);
    
    return KetChuyenChiPhiCongTrinhView;
});
