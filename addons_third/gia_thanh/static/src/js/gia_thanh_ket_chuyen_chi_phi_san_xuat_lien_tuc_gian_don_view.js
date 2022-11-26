odoo.define('gia_thanh.ket_chuyen_chi_phi_san_xuat_lien_tuc_gian_don_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var KetChuyenChiPhiSXLienTucGianDonFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        _onCreate: function() {
            var self = this;

            var domain_san_xuat_lien_tuc_gian_don ='DON_GIAN';

            new dialogs.FormViewDialog(this, {
                tham_so: domain_san_xuat_lien_tuc_gian_don,
                readonly: false,
                res_model: 'gia.thanh.chon.ky.tinh.gia.thanh.ket.chuyen.form',
                ref_views: [['gia_thanh.view_gia_thanh_chon_ky_tinh_gia_thanh_ket_chuyen_form_tham_so_form', 'form']],
                title: ("Chọn kỳ tính giá thành"),
                disable_multiple_selection: true,
                size : 'medium',
                shouldSaveLocally: true,
                on_before_saved: function(controller) {
                    var def = $.Deferred();
                    var ky_tinh_gia_thanh_id = controller.getFieldValue('KY_TINH_GIA_THANH_ID').id;
                    controller.rpc_action({
                        model: 'gia.thanh.chon.ky.tinh.gia.thanh.ket.chuyen.form',
                        method: 'kiem_tra_ket_chuyen_chi_phi',
                        args: {
                            'ky_tinh_gia_thanh_id':ky_tinh_gia_thanh_id,
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
                                            ref_views: [['gia_thanh.view_gia_thanh_ket_chuyen_chi_phi_san_xuat_lien_tuc_gian_don_form', 'form']],
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
                        
                        var context = {
                            'default_KY_TINH_GIA_THANH': ky_tinh_gia_thanh,
                            'default_KY_TINH_GIA_THANH_ID': ky_tinh_gia_thanh_id,
                            
                            'loai_chung_tu': 4080,
                            'loai_ket_chuyen': 'GIAN_DON',
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
                'LOAI_KET_CHUYEN_CHI_PHI': self.params.tham_so['loai_ket_chuyen'],
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
            event.stopPropagation();
            var self = this;
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
    
    var KetChuyenChiPhiSXLienTucGianDonFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
           
            Controller: KetChuyenChiPhiSXLienTucGianDonFormController,
        }),
    });
    
    view_registry.add('ket_chuyen_chi_phi_san_xuat_lien_tuc_gian_don_form_view', KetChuyenChiPhiSXLienTucGianDonFormView);
    
    return KetChuyenChiPhiSXLienTucGianDonFormView;
});
odoo.define('gia_thanh.ket_chuyen_chi_phi_san_xuat_lien_tuc_gian_don_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var KetChuyenChiPhiSXLienTucGianDonController = ListController.extend({
        _onCreate: function() {
            var self = this;

            var domain_san_xuat_lien_tuc_gian_don ='DON_GIAN';

            new dialogs.FormViewDialog(this, {
                tham_so: domain_san_xuat_lien_tuc_gian_don,
                readonly: false,
                res_model: 'gia.thanh.chon.ky.tinh.gia.thanh.ket.chuyen.form',
                ref_views: [['gia_thanh.view_gia_thanh_chon_ky_tinh_gia_thanh_ket_chuyen_form_tham_so_form', 'form']],
                title: ("Chọn kỳ tính giá thành"),
                disable_multiple_selection: true,
                size : 'medium',
                shouldSaveLocally: true,
                on_before_saved: function(controller) {
                    var def = $.Deferred();
                    var ky_tinh_gia_thanh_id = controller.getFieldValue('KY_TINH_GIA_THANH_ID').id;
                    controller.rpc_action({
                        model: 'gia.thanh.chon.ky.tinh.gia.thanh.ket.chuyen.form',
                        method: 'kiem_tra_ket_chuyen_chi_phi',
                        args: {
                            'ky_tinh_gia_thanh_id':ky_tinh_gia_thanh_id,
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
                                            ref_views: [['gia_thanh.view_gia_thanh_ket_chuyen_chi_phi_san_xuat_lien_tuc_gian_don_form', 'form']],
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
                        var context = {
                            'default_KY_TINH_GIA_THANH': ky_tinh_gia_thanh,
                            'default_KY_TINH_GIA_THANH_ID': ky_tinh_gia_thanh_id,
                            'loai_chung_tu': 4080,
                            'loai_ket_chuyen': 'GIAN_DON',
                            'form_them_moi' : true,
                            'ky_tinh_gia_thanh_id' : ky_tinh_gia_thanh_id,
                        }
                        self.createRecord(context);
                    }
                },
               
            }).open();
            
        },
    });
    
    var KetChuyenChiPhiSXLienTucGianDonView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: KetChuyenChiPhiSXLienTucGianDonController,
        }),
    });
    
    view_registry.add('ket_chuyen_chi_phi_san_xuat_lien_tuc_gian_don_list_view', KetChuyenChiPhiSXLienTucGianDonView);
    
    return KetChuyenChiPhiSXLienTucGianDonView;
});