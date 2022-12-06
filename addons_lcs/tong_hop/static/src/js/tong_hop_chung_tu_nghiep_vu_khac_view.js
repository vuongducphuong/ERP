odoo.define('tong_hop.tong_hop_chung_tu_nghiep_vu_khac_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var TongHopChungTuNghiepVuKhacController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        onViewLoaded: function (e, defer) {
            var def = defer;
            var self = this;
            if (this.params) {
                var update_list = {}
                // chứng từ nghiệp vụ khác bù trừ công nợ
                if (this.params.param_bu_tru_cong_no) {
                    var du_lieu = this.params.param_bu_tru_cong_no;
                    if (du_lieu[4].arr_chung_tu.length > 0) {
                        var ngay_hach_toan;
                        var ngay_chung_tu;
                        var so_chung_tu;
                        // var doi_tuong_id;
                        // var currency_id;
                        var tong_tien = 0;
                        var tong_tien_quy_doi = 0;
                        if (du_lieu[2].arr_hach_toan[1][2].SO_TIEN_QUY_DOI) {
                            tong_tien = du_lieu[2].arr_hach_toan[1][2].SO_TIEN;
                            tong_tien_quy_doi = du_lieu[2].arr_hach_toan[1][2].SO_TIEN_QUY_DOI;
                        }
                        if (this.getFieldValue('NGAY_HACH_TOAN')) {
                            ngay_hach_toan = this.getFieldValue('NGAY_HACH_TOAN');
                        }
                        if (this.getFieldValue('NGAY_CHUNG_TU')) {
                            ngay_chung_tu = this.getFieldValue('NGAY_CHUNG_TU');
                        }
                        if (this.getFieldValue('SO_CHUNG_TU')) {
                            so_chung_tu = this.getFieldValue('SO_CHUNG_TU');
                        }
                        // if(this.getFieldValue('DOI_TUONG_ID')){
                        //     doi_tuong_id = this.getFieldValue('DOI_TUONG_ID').id;
                        // }
                        // if (this.getFieldValue('currency_id')) {
                        //     currency_id = this.getFieldValue('currency_id').id;
                        // }
                        for (var i in du_lieu[4].arr_chung_tu) {
                            if (i != 0) {
                                var dict_chung_tu_phai_thu = du_lieu[4].arr_chung_tu[i];
                                dict_chung_tu_phai_thu[2]['NGAY_CHUNG_TU_THANH_TOAN'] = ngay_chung_tu;
                                dict_chung_tu_phai_thu[2]['NGAY_HACH_TOAN_THANH_TOAN'] = ngay_hach_toan;
                                dict_chung_tu_phai_thu[2]['SO_CHUNG_TU_THANH_TOAN'] = so_chung_tu;
                                dict_chung_tu_phai_thu[2]['SO_CHUA_THANH_TOAN'] = tong_tien;
                                dict_chung_tu_phai_thu[2]['SO_CHUA_THANH_TOAN_QUY_DOI'] = tong_tien_quy_doi;
                                // dict_chung_tu_phai_thu['NGAY_CHUNG_TU_THANH_TOAN'] = currency_id;
                            }
                        }
                    };
                    this.changeSelectionSource('CHI_TIET_NGHIEP_VU_KHAC', ['HACH_TOAN']);
                    update_list = {
                        'TONG_HOP_CHUNG_TU_NVK_BU_TRU_CHI_TIET_IDS': du_lieu[3].arr_chung_tu_cong_no,
                        // 'SALE_EX_DOI_TRU_CHI_TIET_IDS': du_lieu[3].arr_chung_tu_cong_no,
                        'ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS': du_lieu[2].arr_hach_toan,
                        'LOAI_CHUNG_TU_QTTU_NVK': 'BU_TRU_CN',
                        'DOI_TUONG_ID': du_lieu[1].dich_du_lieu_master.DOI_TUONG_ID,
                        'LOAI_CHUNG_TU': 4014,
                        'TEN_DOI_TUONG': du_lieu[1].dich_du_lieu_master.TEN_DOI_TUONG,
                        'DIEN_GIAI': du_lieu[1].dich_du_lieu_master.LY_DO,
                        'TK_XU_LY_LAI_ID': du_lieu[1].dich_du_lieu_master.TAI_KHOAN_PHAI_THU,
                        'TK_XU_LY_LO_ID': du_lieu[1].dich_du_lieu_master.TAI_KHOAN_PHAI_TRA,
                        'currency_id': du_lieu[1].dich_du_lieu_master.currency_id,
                        'SALE_EX_DOI_TRU_CHI_TIET_IDS': du_lieu[4].arr_chung_tu,
                    }
                } 
                // xử lý chênh lệch tỷ giá từ đối trừ chứng từ
                if(this.params.param_doi_tru_chung_tu){
                    var du_lieu = this.params.param_doi_tru_chung_tu;
                    this.changeSelectionSource('CHI_TIET_NGHIEP_VU_KHAC', ['HACH_TOAN']);
                    update_list = {
                        'ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS': du_lieu[2].arr_hach_toan,
                        'LOAI_CHUNG_TU_QTTU_NVK': 'XU_LY_CHENH_LECH_TY_GIA',
                        'LOAI_CHUNG_TU': 4013,
                        'LA_TIEN_CO_SO' : false,
                        'TEN_DOI_TUONG': du_lieu[1].dich_du_lieu_master.TEN_DOI_TUONG,
                        'DIEN_GIAI': du_lieu[1].dich_du_lieu_master.LY_DO,
                        'TK_XU_LY_LO_ID': du_lieu[1].dich_du_lieu_master.TK_XU_LY_LO_ID,
                        'currency_id': du_lieu[1].dich_du_lieu_master.currency_id,
                        'SALE_EX_DOI_TRU_CHI_TIET_IDS': du_lieu[3].arr_chung_tu_cong_no,
                        'NGAY_DOI_TRU' : du_lieu[1].dich_du_lieu_master.NGAY_DOI_TRU,
                    }
                }
                // Xử lý chênh lệch tỷ giá từ tỷ giá xuất quỹ
                if(this.params.param_xu_ly_chenh_lech_ty_gia){
                    var du_lieu = this.params.param_xu_ly_chenh_lech_ty_gia;
                    this.changeSelectionSource('CHI_TIET_NGHIEP_VU_KHAC', ['HACH_TOAN']);
                    update_list = {
                        'ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS': du_lieu[1],
                        'LOAI_CHUNG_TU_QTTU_NVK': 'XU_LY_CHENH_LECH_TY_GIA_XUAT_QUY',
                        'LOAI_CHUNG_TU': 4017,
                        'DIEN_GIAI': du_lieu[0].DIEN_GIAI,
                        'THANG': du_lieu[0].THANG,
                        'NAM': du_lieu[0].NAM,
                        'NGAY_CHUNG_TU': du_lieu[0].NGAY_CHUNG_TU,
                        'NGAY_HACH_TOAN': du_lieu[0].NGAY_HACH_TOAN,
                    }
                }
                else {
                    if (this.params.params && this.params.params.LOAI_CHUNG_TU_DANH_GIA_LAI) {
                        var gia_tri_params = this.params.params;
                        update_list['LOAI_CHUNG_TU_QTTU_NVK'] = gia_tri_params.LOAI_CHUNG_TU_DANH_GIA_LAI;
                        update_list['TK_XU_LY_LAI_ID'] = gia_tri_params.TK_XU_LY_LAI_CHENH_LECH_TY_GIA_ID;
                        update_list['TK_XU_LY_LO_ID'] = gia_tri_params.TK_XU_LY_LO_CHENH_LECH_TY_GIA_ID;
                        update_list['TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_SO_DU_NGOAI_TE_IDS'] = gia_tri_params.TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_SO_DU_NGOAI_TE_IDS;
                        update_list['TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_CONG_NO_THANH_TOAN_IDS'] = gia_tri_params.TONG_HOP_CHUNG_TU_NGHIEP_VU_KHAC_CONG_NO_THANH_TOAN_IDS;
                        update_list['ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS'] = gia_tri_params.ACCOUNT_EX_CHUNG_TU_NGHIEP_VU_KHAC_HACH_TOAN_IDS;
                    }
                    if (this.params.params && this.params.params.LOAI_TO_KHAI) {
                        update_list['LOAI_TO_KHAI'] = this.params.params.LOAI_TO_KHAI;
                    }
                    if (this.params.params && this.params.params.QUY) {
                        update_list['KY_TINH_THUE_QUY'] = this.params.params.QUY;
                    }
                    if (this.params.params && this.params.params.THANG) {
                        update_list['KY_TINH_THUE_THANG'] = this.params.params.THANG;
                    }
                    if (this.params.params && this.params.params.NAM) {
                        update_list['NAM'] = this.params.params.NAM;
                    }
                }
                this.updateUI(update_list).then(function () {
                    def.resolve();
                })
            } else {
                def.resolve();
            }
        },
        // onFieldChanged: function(field){
        //     var self =this;
        //     var loai_chung_tu = this.getFieldValue('LOAI_CHUNG_TU');
        //     if(loai_chung_tu){
        //         if(loai_chung_tu == 4014){
        //             if("NGAY_HACH_TOAN" == field || "NGAY_CHUNG_TU" == field || "SO_CHUNG_TU" == field || "DOI_TUONG_ID" == field){
        //                 var doi_tru_chi_tiet = this.getFieldValue('SALE_EX_DOI_TRU_CHI_TIET_IDS');
        //                 var ngay_hach_toan = this.getFieldValue('NGAY_HACH_TOAN');
        //                 var ngay_chung_tu = this.getFieldValue('NGAY_CHUNG_TU');
        //                 var so_chung_tu = this.getFieldValue('SO_CHUNG_TU');
        //                 var doi_tuong_id = this.getFieldValue('DOI_TUONG_ID');
        //                 var doi_tru_chi_tiet_moi = [[5]];
        //                 if(doi_tru_chi_tiet){
        //                     for(var i in doi_tru_chi_tiet){
        //                         var newval = doi_tru_chi_tiet[i];
        //                         if(ngay_hach_toan){
        //                             _.extend(newval,{'NGAY_HACH_TOAN_THANH_TOAN': ngay_hach_toan});
        //                         };
        //                         if(ngay_chung_tu){
        //                             _.extend(newval,{'NGAY_CHUNG_TU_THANH_TOAN': ngay_chung_tu});
        //                         };
        //                         if(so_chung_tu){
        //                             _.extend(newval,{'SO_CHUNG_TU_THANH_TOAN': so_chung_tu});
        //                         };
        //                         if(doi_tuong_id){
        //                             _.extend(newval,{'DOI_TUONG_ID': doi_tuong_id.id});
        //                         };
        //                         doi_tru_chi_tiet_moi.push([0, 0, newval]);
        //                     }
        //                 }
        //                 self.updateUI({'SALE_EX_DOI_TRU_CHI_TIET_IDS': doi_tru_chi_tiet_moi});   
        //             }
        //         }
        //     }

        // },

    });

    var TongHopChungTuNghiepVuKhacRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var TongHopChungTuNghiepVuKhacModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var TongHopChungTuNghiepVuKhacView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: TongHopChungTuNghiepVuKhacModel,
            Renderer: TongHopChungTuNghiepVuKhacRenderer,
            Controller: TongHopChungTuNghiepVuKhacController,
        }),
    });

    view_registry.add('tong_hop_chung_tu_nghiep_vu_khac_view', TongHopChungTuNghiepVuKhacView);

    return TongHopChungTuNghiepVuKhacView;
});
