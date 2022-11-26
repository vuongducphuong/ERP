odoo.define('gia_thanh.ky_tinh_gia_thanh_san_xuat_lien_tuc_he_so_ty_le_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var KyTinhGiaThanhSanXuatLienTucHeSoTyLeFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        _onButtonClicked: function(event) {
            
            event.stopPropagation();
            var self = this;
            switch (event.data.attrs.id)
            {
                case "btn_tinh_gia_thanh":
                    var ten = this.getFieldValue('TEN');
                    var ky_tinh_gia_thanh_id;
                    if(event.data.record.res_id){
                        ky_tinh_gia_thanh_id = event.data.record.res_id;
                    }
                    var tu_ngay = this.getFieldValue('TU_NGAY');
                    var den_ngay = this.getFieldValue('DEN_NGAY');
                    var loai_tinh_gia_thanh = 'HE_SO_TY_LE';
                    new dialogs.FormViewDialog(this, {
                        tham_so : ten,
                        ky_tinh_gia_thanh_id : ky_tinh_gia_thanh_id,
                        tu_ngay : tu_ngay,
                        den_ngay : den_ngay,
                        loai_tinh_gia_thanh : loai_tinh_gia_thanh,
                        readonly: false,
                        res_model: 'gia.thanh.tinh.gia.thanh',
                        ref_views: [['gia_thanh.view_gia_thanh_tinh_gia_thanh_san_xuat_lien_tuc_he_so_ty_le_tham_so_form', 'form']],
                        title: 'Tính giá thành sản xuất liên tục - Hệ số, tỷ lệ',
                        disable_multiple_selection: true,
                        shouldSaveLocally: false,
                        // on_saved: function (record, changed) {
                                //     if (changed) {
                                //         self.cReload();
                                //     }
                                // },
                    }).open();
                    break;
                case "btn_tap_hop_chi_phi_truc_tiep":
                    var ten = this.getFieldValue('TEN');
                    var ky_tinh_gia_thanh_id = event.data.record.data.id;
                    new dialogs.FormViewDialog(this, {
                        tham_so : ten,
                        ky_tinh_gia_thanh_id : ky_tinh_gia_thanh_id,
                        readonly: false,
                        res_model: 'gia.thanh.tap.hop.chi.phi.truc.tiep',
                        ref_views: [['gia_thanh.view_gia_thanh_tap_hop_chi_phi_truc_tiep_san_xuat_lien_tuc_he_so_ty_le_tham_so_form', 'form']],
                        title: 'Tập hợp chi phí trực tiếp',
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        // on_saved: function (record, changed) {
                                //     if (changed) {
                                //         self.cReload();
                                //     }
                                // },
                    }).open();
                    break;
                case "btn_tap_hop_khoan_giam_gia_thanh":
                    var ten = this.getFieldValue('TEN');
                    var ky_tinh_gia_thanh_id = event.data.record.data.id;
                    new dialogs.FormViewDialog(this, {
                        tham_so : ten,
                        ky_tinh_gia_thanh_id : ky_tinh_gia_thanh_id,
                        readonly: false,
                        res_model: 'gia.thanh.tap.hop.khoan.giam.gia.thanh',
                        ref_views: [['gia_thanh.view_gia_thanh_tap_hop_khoan_giam_gia_thanh_san_xuat_lien_tuc_he_so_ty_le_tham_so_form', 'form']],
                        title: 'Tập hợp khoản giảm giá thành',
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        // on_saved: function (record, changed) {
                                //     if (changed) {
                                //         self.cReload();
                                //     }
                                // },
                    }).open();
                    break;
                case "btn_bang_tap_hop_chi_phi_theo_yeu_to":
                    var ten = this.getFieldValue('TEN');
                    var ky_tinh_gia_thanh_id = event.data.record.data.id;
                    new dialogs.FormViewDialog(this, {
                        tham_so : ten,
                        ky_tinh_gia_thanh_id : ky_tinh_gia_thanh_id,
                        readonly: false,
                        res_model: 'gia.thanh.bang.tap.hop.chi.phi.theo.yeu.to',
                        ref_views: [['gia_thanh.view_gia_thanh_bang_tap_hop_chi_phi_theo_yeu_to_san_xuat_lien_tuc_he_so_ty_le_tham_so_form', 'form']],
                        title: 'Bảng tập hợp chi phí theo yếu tố',
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        // on_saved: function (record, changed) {
                                //     if (changed) {
                                //         self.cReload();
                                //     }
                                // },
                    }).open();
                    break;
                case "btn_bang_tap_hop_chi_phi_theo_khoan_muc":
                    var ten = this.getFieldValue('TEN');
                    var ky_tinh_gia_thanh_id = event.data.record.data.id;
                    new dialogs.FormViewDialog(this, {
                        tham_so : ten,
                        ky_tinh_gia_thanh_id : ky_tinh_gia_thanh_id,
                        readonly: false,
                        res_model: 'gia.thanh.bang.tap.hop.chi.phi.theo.khoan.muc',
                        ref_views: [['gia_thanh.view_gia_thanh_bang_tap_hop_chi_phi_theo_khoan_muc_san_xuat_lien_tuc_he_so_ty_le_tham_so_form', 'form']],
                        title: 'Bảng tập hợp chi phí theo khoản mục',
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        // on_saved: function (record, changed) {
                                //     if (changed) {
                                //         self.cReload();
                                //     }
                                // },
                    }).open();
                    break;
                case "btn_ket_chuyen_chi_phi":
                        var context = {
                            'ten': this.getFieldValue('TEN'),
                            'tu_ngay':this.getFieldValue('TU_NGAY'),
                            'den_ngay':this.getFieldValue('DEN_NGAY'),
                            'loai_chung_tu': 4080,
                            'loai_ket_chuyen': 'HE_SO_TY_LE',
                            'id_ky_tinh_gia_thanh':event.data.record.data.id,
                            };
                        var ky_tinh_gia_thanh_id = event.data.record.data.id;
                        self.rpc_action({
                            model: 'gia.thanh.ky.tinh.gia.thanh',
                            method: 'kiem_tra_ton_tai_ket_chuyen',
                            args: {
                                'id_ky_tinh_gia_thanh':ky_tinh_gia_thanh_id,
                            },
                            callback: function(result) {
                                if (result == 0) {
                                    // var options = {
                                    //     context : context,
                                    //     params : ky_tinh_gia_thanh_id,
                                    //     res_model: 'gia.thanh.ket.chuyen.chi.phi',
                                    //     ref_view: 'gia_thanh.view_gia_thanh_ket_chuyen_chi_phi_san_xuat_lien_tuc_he_so_ty_le_form',
                                    //     // res_id:result,
                                    //     title: 'Kết chuyển chi phí',
                                    // }
                                    // return self.openFormView(options);
                                    new dialogs.FormViewDialog(self, {
                                        context : context,
                                        ky_tinh_gia_thanh_id : ky_tinh_gia_thanh_id,
                                        form_them_moi : true,
                                        readonly: false,
                                        res_model: 'gia.thanh.ket.chuyen.chi.phi',
                                        ref_views: [['gia_thanh.view_gia_thanh_ket_chuyen_chi_phi_san_xuat_lien_tuc_he_so_ty_le_form', 'form']],
                                        title: 'Kết chuyển chi phí',
                                        disable_multiple_selection: true,
                                        shouldSaveLocally: false,
                                
                                    }).open();
                                }
                                else{
                                    Dialog.show_message('', 'Đã tồn tại chứng từ kết chuyển chi phí của kỳ tính giá thành này. Bạn có muốn xem chứng từ này không?', 'CONFIRM')
                                    .then(function(result_yes_no) {
                                        if (result_yes_no == true){
                                            var options = {
                                                res_model: 'gia.thanh.ket.chuyen.chi.phi',
                                                ref_view: 'gia_thanh.view_gia_thanh_ket_chuyen_chi_phi_san_xuat_lien_tuc_he_so_ty_le_form',
                                                res_id:result,
                                                title: 'Kết chuyển chi phí',
                                            }
                                            return self.openFormView(options);
                                        }
                                    });
                        
                            
                                }         
                        }});
                        
                        break;
                case "btn_chon":
                    new dialogs.FormViewDialog(this, {
                        // tham_so : dict_param,
                        readonly: false,
                        res_model: 'gia.thanh.chon.doi.tuong.can.tap.hop.chi.phi.form',
                        ref_views: [['gia_thanh.view_gia_thanh_chon_doi_tuong_can_tap_hop_chi_phi_san_xuat_lien_tuc_he_so_ty_le_form', 'form']],
                        title: 'Chọn đối tượng cần tập hợp chi phí',
                        size : 'large',
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        on_after_saved: function(record, changes) {
                            if(changes){
                                var default_doi_tuong_thcp  =[[5]];
                                

                                var current_data = record.data;
                                var chitiet_ids = current_data.GIA_THANH_CHON_DOI_TUONG_CAN_TAP_HOP_CHI_PHI_CHI_TIET_IDS.data;
                                for(var i=0;i<chitiet_ids.length;i++)
                                {
                                    
                                    //chỉ lấy những thằng chọn
                                    var chi_tiet = chitiet_ids[i].data;
                                    if (chi_tiet.AUTO_SELECT)
                                    {
                                        default_doi_tuong_thcp.push([0, 0, {
                                            'MA_DOI_TUONG_THCP_ID': [chi_tiet.MA_SAN_PHAM_ID.data.id,chi_tiet.MA_SAN_PHAM_ID.data.display_name],
                                            'TEN_DOI_TUONG_THCP': chi_tiet.TEN_SAN_PHAM ,
                                            'LOAI': chi_tiet.LOAI,
                                    }])
                                    }

                                }
                                self.updateUI({'GIA_THANH_KY_TINH_GIA_THANH_CHI_TIET_IDS':default_doi_tuong_thcp,});

    
                        }
                    }
                    }).open();
                    break;
                default: 
                   this._super.apply(this, arguments);
            }
            
        },
    });

    var KyTinhGiaThanhSanXuatLienTucHeSoTyLeFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: KyTinhGiaThanhSanXuatLienTucHeSoTyLeFormController,
        }),
    });
    
    view_registry.add('ky_tinh_gia_thanh_san_xuat_lien_tuc_he_so_ty_le_form_view', KyTinhGiaThanhSanXuatLienTucHeSoTyLeFormView);
    
    return KyTinhGiaThanhSanXuatLienTucHeSoTyLeFormView;
});
