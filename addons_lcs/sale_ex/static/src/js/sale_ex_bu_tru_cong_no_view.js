odoo.define('sale_ex.bu_tru_cong_no_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var Dialog = require('web.Dialog');

    var BuTruCongNoController = FormController.extend({
        custom_events: _.extend({}, FormController.prototype.custom_events, {
            on_selections_changed: '_onSelectionsChanged',
        }),
        _onButtonClicked: function (event) {
            var self = this;
            event.stopPropagation();
            switch (event.data.attrs.id) {
                case "btn_bu_tru":
                    var chung_tu_phai_thu = this.getFieldValue('SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS');
                    var chung_tu_phai_tra = this.getFieldValue('SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS');
                    var arr_hach_toan = [[5]];
                    var param_tham_so = [[5]];
                    var arr_chung_tu_cong_no = [[5]];
                    var tong_tien_doi_tru_phai_thu = 0;
                    var tong_tien_doi_tru_phai_tra = 0;
                    var tong_tien_doi_tru_quy_doi = 0;
                    var arr_chung_tu = [[5]];
                    // var arr_chung_tu_phai_thu = [[5]];
                    var dich_du_lieu_master
                    if (chung_tu_phai_thu.length > 0 && chung_tu_phai_tra.length > 0) {
                        var doi_tuong = this.getFieldValue('DOI_TUONG_ID');
                        dich_du_lieu_master = {
                            'DOI_TUONG_ID': doi_tuong,
                            'TEN_DOI_TUONG': doi_tuong.display_name,
                            'LY_DO': 'Bù trừ công nợ phải thu, phải trả với' + doi_tuong.display_name,
                            'TAI_KHOAN_PHAI_THU': this.getFieldValue('TK_PHAI_THU_ID'),
                            'TAI_KHOAN_PHAI_TRA': this.getFieldValue('TK_PHAI_TRA_ID'),
                            'NGAY_BU_TRU': this.getFieldValue('NGAY_BU_TRU'),
                            'currency_id': this.getFieldValue('currency_id'),
                            'LOAI_CHUNG_TU': 4014,
                        }
                        param_tham_so.push({ 'dich_du_lieu_master': dich_du_lieu_master });
                        var tk_phai_thu;
                        var tk_phai_tra;
                        var currency_id;
                        var doi_tuong_id;
                        var chenh_lech_bu_tru_cong_no = 0;
                        if (this.getFieldValue('currency_id')) {
                            currency_id = this.getFieldValue('currency_id').id;
                        }
                        if (this.getFieldValue('DOI_TUONG_ID')) {
                            doi_tuong_id = this.getFieldValue('DOI_TUONG_ID').id;
                        }
                        if (this.getFieldValue('TK_PHAI_THU_ID')) {
                            tk_phai_thu = this.getFieldValue('TK_PHAI_THU_ID').id;
                        }
                        if (this.getFieldValue('TK_PHAI_TRA_ID')) {
                            tk_phai_tra = this.getFieldValue('TK_PHAI_TRA_ID').id;
                        }
                        if (this.getFieldValue('CHENH_LECH_BU_TRU_QUY_DOI')) {
                            chenh_lech_bu_tru_cong_no = this.getFieldValue('CHENH_LECH_BU_TRU_QUY_DOI');
                        }


                        var so_dong_tich_chon_phai_thu = 0;
                        var so_dong_tich_chon_phai_tra = 0;
                        for (var i in chung_tu_phai_thu) {
                            if (chung_tu_phai_thu[i].AUTO_SELECT == true) {
                                so_dong_tich_chon_phai_thu += 1;
                                if (chung_tu_phai_thu[i].SO_TIEN_BU_TRU) {
                                    tong_tien_doi_tru_phai_thu += chung_tu_phai_thu[i].SO_TIEN_BU_TRU;
                                    tong_tien_doi_tru_quy_doi += chung_tu_phai_thu[i].SO_TIEN_BU_TRU_QUY_DOI;
                                }
                            }
                        };

                        for (var j in chung_tu_phai_tra) {
                            if (chung_tu_phai_tra[j].AUTO_SELECT == true) {
                                so_dong_tich_chon_phai_tra += 1;
                                if (chung_tu_phai_tra[j].SO_TIEN_BU_TRU) {
                                    tong_tien_doi_tru_phai_tra += chung_tu_phai_tra[j].SO_TIEN_BU_TRU;
                                }
                            }
                        }
                        if (so_dong_tich_chon_phai_thu == 0 || so_dong_tich_chon_phai_tra == 0) {
                            Dialog.show_message('Thông báo', 'Bạn phải chọn các chứng từ để thực hiện đối trừ', 'ALERT')
                                .then(function (result) {
                                    return;
                                });

                            return;
                        }
                        if (tong_tien_doi_tru_phai_thu != tong_tien_doi_tru_phai_tra) {
                            Dialog.show_message('Thông báo', 'Tổng số tiền bù trừ của <Chứng từ phải thu> phải bằng tổng số tiền bù trừ của <Chứng từ phải trả>', 'ALERT')
                                .then(function (result) {
                                    return;
                                });

                            return;
                        }

                        var so_con_no_cho_debt = tong_tien_doi_tru_phai_thu;
                        var so_con_no_cho_debt_quy_doi = tong_tien_doi_tru_quy_doi;
                        // var so_chua_thu_cho_phai_thu = tong_tien_doi_tru_phai_thu;
                        for (var i in chung_tu_phai_thu) {
                            var chi_tiet_phai_thu = chung_tu_phai_thu[i];
                            if (chi_tiet_phai_thu.AUTO_SELECT == true) {

                                for (var j in chung_tu_phai_tra) {
                                    var chi_tiet_phai_tra = chung_tu_phai_tra[j];
                                    var so_tien_doi_tru;
                                    var so_tien_doi_tru_quy_doi;
                                    if (chi_tiet_phai_tra.AUTO_SELECT == true) {
                                        if (chi_tiet_phai_thu.SO_TIEN_BU_TRU > 0 && chi_tiet_phai_tra.SO_TIEN_BU_TRU > 0) {
                                            if (chi_tiet_phai_thu.SO_TIEN_BU_TRU > chi_tiet_phai_tra.SO_TIEN_BU_TRU) {
                                                so_tien_doi_tru = chi_tiet_phai_tra.SO_TIEN_BU_TRU;
                                                so_tien_doi_tru_quy_doi = chi_tiet_phai_tra.SO_TIEN_BU_TRU_QUY_DOI;
                                            }
                                            else if (chi_tiet_phai_thu.SO_TIEN_BU_TRU == chi_tiet_phai_tra.SO_TIEN_BU_TRU) {
                                                so_tien_doi_tru = chi_tiet_phai_tra.SO_TIEN_BU_TRU;
                                                so_tien_doi_tru_quy_doi = chi_tiet_phai_tra.SO_TIEN_BU_TRU_QUY_DOI;
                                            }
                                            else {
                                                so_tien_doi_tru = chi_tiet_phai_thu.SO_TIEN_BU_TRU;
                                                so_tien_doi_tru_quy_doi = chi_tiet_phai_thu.SO_TIEN_BU_TRU_QUY_DOI;
                                            }
                                            chi_tiet_phai_thu.SO_TIEN_BU_TRU = chi_tiet_phai_thu.SO_TIEN_BU_TRU - so_tien_doi_tru;
                                            chi_tiet_phai_tra.SO_TIEN_BU_TRU = chi_tiet_phai_tra.SO_TIEN_BU_TRU - so_tien_doi_tru;
                                            chi_tiet_phai_thu.SO_TIEN_BU_TRU_QUY_DOI = chi_tiet_phai_thu.SO_TIEN_BU_TRU_QUY_DOI - so_tien_doi_tru_quy_doi;
                                            chi_tiet_phai_tra.SO_TIEN_BU_TRU_QUY_DOI = chi_tiet_phai_tra.SO_TIEN_BU_TRU_QUY_DOI - so_tien_doi_tru_quy_doi;


                                            var dict_bu_tru_cong_no_phai_thu = {
                                                'NGAY_CHUNG_TU_THANH_TOAN': chi_tiet_phai_thu.NGAY_CHUNG_TU,
                                                'SO_CHUNG_TU_THANH_TOAN': chi_tiet_phai_thu.SO_CHUNG_TU,
                                                'SO_CHUA_THANH_TOAN': chi_tiet_phai_thu.SO_TIEN,
                                                'SO_CHUA_THANH_TOAN_QUY_DOI': chi_tiet_phai_thu.SO_TIEN_QUY_DOI,
                                                'SO_TIEN_THANH_TOAN': chi_tiet_phai_thu.SO_CHUA_THU,
                                                'SO_TIEN_THANH_TOAN_QUY_DOI': chi_tiet_phai_thu.SO_CHUA_THU_QUY_DOI,
                                                'SO_THANH_TOAN_LAN_NAY': so_tien_doi_tru,
                                                'SO_THANH_TOAN_LAN_NAY_QUY_DOI': so_tien_doi_tru_quy_doi,
                                                'SO_THANH_TOAN_LAN_NAY_QUY_DOI': chi_tiet_phai_thu.SO_TIEN_BU_TRU_QUY_DOI,
                                                'ID_CHUNG_TU_THANH_TOAN': chi_tiet_phai_thu.ID_GOC,
                                                'MODEL_CHUNG_TU_THANH_TOAN': chi_tiet_phai_thu.MODEL_GOC,
                                                'TEN_LOAI_CHUNG_TU_THANH_TOAN': chi_tiet_phai_thu.TEN_LOAI_CHUNG_TU,
                                                'SO_HOA_DON_THANH_TOAN': chi_tiet_phai_thu.SO_HOA_DON,

                                                'NGAY_CHUNG_TU_CONG_NO': chi_tiet_phai_tra.NGAY_CHUNG_TU,
                                                'SO_CHUNG_TU_CONG_NO': chi_tiet_phai_tra.SO_CHUNG_TU,
                                                'SO_HOA_DON_CONG_NO': chi_tiet_phai_tra.SO_HOA_DON,
                                                'SO_TIEN_CON_NO': chi_tiet_phai_tra.SO_TIEN,
                                                'SO_TIEN_CON_NO_QUY_DOI': chi_tiet_phai_tra.SO_TIEN_QUY_DOI,
                                                'SO_TIEN_CONG_NO': chi_tiet_phai_tra.SO_CON_NO,
                                                'SO_TIEN_CONG_NO_QUY_DOI': chi_tiet_phai_tra.SO_CON_NO_QUY_DOI,
                                                'SO_CONG_NO_THANH_TOAN_LAN_NAY': so_tien_doi_tru,
                                                'SO_CONG_NO_THANH_TOAN_LAN_NAY_QUY_DOI': so_tien_doi_tru_quy_doi,
                                                'SO_CONG_NO_THANH_TOAN_LAN_NAY_QUY_DOI': chi_tiet_phai_tra.SO_TIEN_BU_TRU_QUY_DOI,
                                                'TEN_LOAI_CHUNG_TU_CONG_NO': chi_tiet_phai_tra.TEN_LOAI_CHUNG_TU,
                                                'ID_CHUNG_TU_CONG_NO': chi_tiet_phai_tra.ID_GOC,
                                                'MODEL_CHUNG_TU_CONG_NO': chi_tiet_phai_tra.MODEL_GOC,
                                                'LOAI_DOI_TRU': '2',
                                                'HIEN_TREN_BU_TRU': false,
                                                'TAI_KHOAN_ID': tk_phai_thu,
                                                'currency_id': currency_id,
                                                'CTCN_DA_GHI_SO': true,
                                                'CTTT_DA_GHI_SO': true,
                                                'DOI_TUONG_ID': doi_tuong_id,
                                            }
                                            arr_chung_tu_cong_no.push([0, 0, dict_bu_tru_cong_no_phai_thu]);

                                            // SO_CHUA_THANH_TOAN - TotalPayableAmount
                                            // SO_TIEN_THANH_TOAN - PayableAmount
                                            // SO_THANH_TOAN_LAN_NAY - PayAmount

                                            // SO_TIEN_CON_NO - TotalDebtableAmount
                                            // SO_TIEN_CONG_NO - DebtAmount
                                            // SO_CONG_NO_THANH_TOAN_LAN_NAY - DebtableAmount
                                            var dict_chung_tu_phai_tra = {
                                                'SO_TIEN_CON_NO': chi_tiet_phai_tra.SO_TIEN,
                                                'SO_TIEN_CON_NO_QUY_DOI': chi_tiet_phai_tra.SO_TIEN_QUY_DOI,
                                                'SO_TIEN_CONG_NO': chi_tiet_phai_tra.SO_CON_NO,
                                                'SO_TIEN_CONG_NO_QUY_DOI': chi_tiet_phai_tra.SO_CON_NO_QUY_DOI,
                                                'SO_CONG_NO_THANH_TOAN_LAN_NAY': so_tien_doi_tru,
                                                'SO_CONG_NO_THANH_TOAN_LAN_NAY_QUY_DOI': so_tien_doi_tru_quy_doi,

                                                'SO_TIEN_THANH_TOAN': so_con_no_cho_debt,
                                                'SO_TIEN_THANH_TOAN_QUY_DOI': so_con_no_cho_debt_quy_doi,
                                                'SO_THANH_TOAN_LAN_NAY': so_tien_doi_tru,
                                                'SO_THANH_TOAN_LAN_NAY_QUY_DOI': so_tien_doi_tru_quy_doi,

                                                'SO_CHUNG_TU_CONG_NO': chi_tiet_phai_tra.SO_CHUNG_TU,
                                                'NGAY_CHUNG_TU_CONG_NO': chi_tiet_phai_tra.NGAY_CHUNG_TU,
                                                'NGAY_HACH_TOAN_CONG_NO': chi_tiet_phai_tra.NGAY_CHUNG_TU,
                                                'TEN_LOAI_CHUNG_TU_CONG_NO': chi_tiet_phai_tra.LOAI_CHUNG_TU,
                                                'ID_CHUNG_TU_CONG_NO': chi_tiet_phai_tra.ID_GOC,
                                                'MODEL_CHUNG_TU_CONG_NO': chi_tiet_phai_tra.MODEL_GOC,
                                                'LOAI_DOI_TRU': '2',
                                                'TAI_KHOAN_ID': tk_phai_thu,
                                                'currency_id': currency_id,
                                                'CTCN_DA_GHI_SO': true,
                                                'CTTT_DA_GHI_SO': false,
                                                'DOI_TUONG_ID': doi_tuong_id,
                                                // 'TEN_LOAI_CHUNG_TU_THANH_TOAN' : chi_tiet_phai_tra.LOAI_CHUNG_TU,
                                                'TAI_KHOAN_ID': tk_phai_tra,
                                                'LOAI_CHUNG_TU_THANH_TOAN': 4014,
                                                'LOAI_CHUNG_TU_CONG_NO': chi_tiet_phai_tra.LOAI_CHUNG_TU,
                                                'NGAY_HOA_DON_CONG_NO': chi_tiet_phai_tra.NGAY_HOA_DON,
                                            }
                                            arr_chung_tu.push([0, 0, dict_chung_tu_phai_tra]);

                                            var dict_chung_tu_phai_thu = {
                                                'SO_TIEN_CON_NO': chi_tiet_phai_thu.SO_TIEN,
                                                'SO_TIEN_CON_NO_QUY_DOI': chi_tiet_phai_thu.SO_TIEN_QUY_DOI,
                                                'SO_TIEN_CONG_NO': chi_tiet_phai_thu.SO_CHUA_THU,
                                                'SO_TIEN_CONG_NO_QUY_DOI': chi_tiet_phai_thu.SO_CHUA_THU_QUY_DOI,
                                                'SO_CONG_NO_THANH_TOAN_LAN_NAY': so_tien_doi_tru,
                                                'SO_CONG_NO_THANH_TOAN_LAN_NAY_QUY_DOI': so_tien_doi_tru_quy_doi,
                                                'SO_TIEN_THANH_TOAN': so_con_no_cho_debt,
                                                'SO_TIEN_THANH_TOAN_QUY_DOI': so_con_no_cho_debt_quy_doi,
                                                'SO_THANH_TOAN_LAN_NAY': so_tien_doi_tru,
                                                'SO_THANH_TOAN_LAN_NAY_QUY_DOI': so_tien_doi_tru_quy_doi,

                                                'NGAY_CHUNG_TU_CONG_NO': chi_tiet_phai_thu.NGAY_CHUNG_TU,
                                                'NGAY_HACH_TOAN_CONG_NO': chi_tiet_phai_thu.NGAY_CHUNG_TU,
                                                'SO_CHUNG_TU_CONG_NO': chi_tiet_phai_thu.SO_CHUNG_TU,
                                                'SO_HOA_DON_CONG_NO': chi_tiet_phai_thu.SO_HOA_DON,
                                                'TEN_LOAI_CHUNG_TU_CONG_NO': chi_tiet_phai_thu.LOAI_CHUNG_TU,
                                                'ID_CHUNG_TU_CONG_NO': chi_tiet_phai_thu.ID_GOC,
                                                'MODEL_CHUNG_TU_CONG_NO': chi_tiet_phai_thu.MODEL_GOC,
                                                'LOAI_DOI_TRU': '2',
                                                'TAI_KHOAN_ID': tk_phai_thu,
                                                'currency_id': currency_id,
                                                'CTCN_DA_GHI_SO': true,
                                                'CTTT_DA_GHI_SO': false,
                                                'DOI_TUONG_ID': doi_tuong_id,
                                                'TAI_KHOAN_ID': tk_phai_thu,
                                                'LOAI_CHUNG_TU_THANH_TOAN': 4014,
                                                'LOAI_CHUNG_TU_CONG_NO': chi_tiet_phai_thu.LOAI_CHUNG_TU,
                                                'NGAY_HOA_DON_CONG_NO': chi_tiet_phai_thu.NGAY_HOA_DON,
                                                // 'TEN_LOAI_CHUNG_TU_THANH_TOAN' : chi_tiet_phai_thu.TEN_LOAI_CHUNG_TU,
                                            }
                                            arr_chung_tu.push([0, 0, dict_chung_tu_phai_thu]);

                                            //giam so chua thu di lan sau
                                            // so_chua_thu_cho_phai_thu = so_chua_thu_cho_phai_thu - so_tien_doi_tru;
                                            so_con_no_cho_debt = so_con_no_cho_debt - so_tien_doi_tru;
                                            so_con_no_cho_debt_quy_doi = so_con_no_cho_debt_quy_doi - so_tien_doi_tru_quy_doi;

                                            if (chi_tiet_phai_thu.SO_TIEN_BU_TRU == 0) break;
                                        }
                                    }
                                }
                            }
                        }
                        arr_hach_toan.push([0, 0, {
                            'DIEN_GIAI': 'Bù trừ công nợ phải thu, phải trả',
                            'SO_TIEN_QUY_DOI': tong_tien_doi_tru_quy_doi,
                            'SO_TIEN': tong_tien_doi_tru_phai_thu,
                            'TK_NO_ID': [this.getFieldValue('TK_PHAI_TRA_ID').id, this.getFieldValue('TK_PHAI_TRA_ID').display_name],
                            'TK_CO_ID': [this.getFieldValue('TK_PHAI_THU_ID').id, this.getFieldValue('TK_PHAI_THU_ID').display_name],

                        }])
                        if (chenh_lech_bu_tru_cong_no != 0) {
                            arr_hach_toan.push([0, 0, {
                                'DIEN_GIAI': 'Bù trừ công nợ phải thu, phải trả',
                                'SO_TIEN_QUY_DOI': chenh_lech_bu_tru_cong_no,
                                'SO_TIEN': 0,
                                'TK_NO_ID': [this.getFieldValue('TK_PHAI_TRA_ID').id, this.getFieldValue('TK_PHAI_TRA_ID').display_name],
                                'TK_CO_ID': [this.getFieldValue('TK_XU_LY_ID').id, this.getFieldValue('TK_XU_LY_ID').display_name],

                            }])
                        }
                        param_tham_so.push({ 'arr_hach_toan': arr_hach_toan });
                        param_tham_so.push({ 'arr_chung_tu_cong_no': arr_chung_tu_cong_no });
                        param_tham_so.push({ 'arr_chung_tu': arr_chung_tu });

                    }


                    var options = {
                        params: { param_bu_tru_cong_no: param_tham_so },
                        res_model: 'account.ex.chung.tu.nghiep.vu.khac',
                        ref_view: 'tong_hop.view_account_ex_chung_tu_nghiep_vu_khac_form',
                        // context: {
                        //     default_SO_CHUNG_TU: '123',
                        // }
                        //                         on_after_saved: function (record, changed) {
                        //                                 if (changed) {
                        //                                     self.cReload();
                        //                                 }
                        //                             },
                    }
                    return this.openFormView(options);

                    break;
                case "btn_lay_du_lieu":
                    var doi_tuong_id = 0;
                    var ngay_bu_tru;
                    var currency_id = 0;



                    // if(null==this.getFieldValue('DOI_TUONG_ID')){
                    //     Dialog.show_message('Cảnh báo', '<Đối tượng> không được bỏ trống.', 'ALERT')
                    //     .then(function(result) {
                    //         // Xử lý sau khi đóng popup
                    //     });
                    // }
                    // if(null==this.getFieldValue('TK_PHAI_THU_ID')){
                    //     Dialog.show_message('Cảnh báo', '<Tài khoản phải thu> không được bỏ trống.', 'ALERT')
                    //     .then(function(result) {
                    //         // Xử lý sau khi đóng popup
                    //     });
                    // }
                    // if(null==this.getFieldValue('TK_PHAI_TRA_ID')){
                    //     Dialog.show_message('Cảnh báo', '<Tài khoản phải trả> không được bỏ trống.', 'ALERT')
                    //     .then(function(result) {
                    //         // Xử lý sau khi đóng popup
                    //     });
                    // }
                    // if(null==this.getFieldValue('NGAY_BU_TRU')){
                    //     Dialog.show_message('Cảnh báo', '<Ngày bù trừ> không được bỏ trống.', 'ALERT')
                    //     .then(function(result) {
                    //         // Xử lý sau khi đóng popup
                    //     });
                    // }
                    // if(null==this.getFieldValue('currency_id')){
                    //     Dialog.show_message('Cảnh báo', '<Loại tiền> không được bỏ trống.', 'ALERT')
                    //     .then(function(result) {
                    //         // Xử lý sau khi đóng popup
                    //     });
                    // }

                    if (this.getFieldValue('DOI_TUONG_ID')) {
                        doi_tuong_id = this.getFieldValue('DOI_TUONG_ID').id;
                    }
                    if (this.getFieldValue('NGAY_BU_TRU')) {
                        ngay_bu_tru = this.getFieldValue('NGAY_BU_TRU');
                    }
                    if (this.getFieldValue('currency_id')) {
                        currency_id = this.getFieldValue('currency_id').id;
                    }
                    this.rpc_action({
                        model: 'sale.ex.bu.tru.cong.no',
                        method: 'lay_du_lieu_doi_tru',
                        args: {
                            'doi_tuong_id': doi_tuong_id,
                            'ngay_bu_tru': ngay_bu_tru,
                            'currency_id': currency_id,
                        },
                        callback: function (result) {
                            if (result) {
                                self.updateUI({
                                    'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS': result.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS,
                                    'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS': result.SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS,
                                });
                            }
                        }
                    });
                    break;
                default:
                    this._super.apply(this, arguments);
            }
        },

        _onSelectionsChanged: function () {
            var self = this;
            var tong_tien_phai_tra = 0;
            var tong_tien_phai_thu = 0;
            var tong_tien_bu_tru_phai_tra_quy_doi = 0;
            var tong_tien_bu_tru_phai_thu_quy_doi = 0;
            var chi_tiet_phai_tra;
            var chi_tiet_phai_thu;
            var ty_gia_de_nhan = 0;
            var chung_tu_phai_thu = this.getFieldValue('SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS');
            var chung_tu_phai_tra = this.getFieldValue('SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS');
            var update_list = {
                'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS': [],
                'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS': [],
            }
            for (var i in chung_tu_phai_tra) {
                if (chung_tu_phai_tra[i].AUTO_SELECT == true) {
                    tong_tien_phai_tra += chung_tu_phai_tra[i].SO_CON_NO
                }
            }
            for (var i in chung_tu_phai_thu) {
                if (chung_tu_phai_thu[i].AUTO_SELECT == true) {
                    tong_tien_phai_thu += chung_tu_phai_thu[i].SO_CHUA_THU
                }
            }

            // TH tích chọn cả hai		
            if (tong_tien_phai_thu > 0 && tong_tien_phai_tra > 0) {
                if (tong_tien_phai_tra > tong_tien_phai_thu) {
                    for (var i in chung_tu_phai_thu) {
                        chi_tiet_phai_thu = chung_tu_phai_thu[i];
                        if (chi_tiet_phai_thu.AUTO_SELECT == true) {
                            if (chi_tiet_phai_thu.TY_GIA_DANH_GIA_LAI > 0) {
                                ty_gia_de_nhan = chung_tu_phai_thu[i].TY_GIA_DANH_GIA_LAI
                            } else {
                                ty_gia_de_nhan = chung_tu_phai_thu[i].TY_GIA
                            }
                            // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS': [[1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': chi_tiet_phai_thu.SO_CHUA_THU, 'SO_TIEN_BU_TRU_QUY_DOI': chi_tiet_phai_thu.SO_CHUA_THU * ty_gia_de_nhan }]] });
                            update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'].push([1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': chi_tiet_phai_thu.SO_CHUA_THU, 'SO_TIEN_BU_TRU_QUY_DOI': chi_tiet_phai_thu.SO_CHUA_THU * ty_gia_de_nhan }]);
                        }
                        if (chung_tu_phai_thu[i].AUTO_SELECT == false) {
                            // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS': [[1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]] });
                            update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'].push([1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]);
                        }
                    }

                    for (var i in chung_tu_phai_tra) {
                        chi_tiet_phai_tra = chung_tu_phai_tra[i];
                        if (chi_tiet_phai_tra.AUTO_SELECT == true) {
                            if (chi_tiet_phai_tra.TY_GIA_DANH_GIA_LAI > 0) {
                                ty_gia_de_nhan = chi_tiet_phai_tra.TY_GIA_DANH_GIA_LAI
                            } else {
                                ty_gia_de_nhan = chi_tiet_phai_tra.TY_GIA
                            };
                            if (tong_tien_phai_thu == 0) {
                                // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS': [[1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]] });
                                update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS'].push([1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]);
                            } else if (chi_tiet_phai_tra.SO_CON_NO < tong_tien_phai_thu) {
                                // self.updateUI({'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS': [[1, chi_tiet_phai_tra.res_id, {'SO_TIEN_BU_TRU': chi_tiet_phai_tra.SO_CON_NO,'SO_TIEN_BU_TRU_QUY_DOI': chi_tiet_phai_tra.SO_CON_NO * ty_gia_de_nhan }]] });
                                update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS'].push([1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': chi_tiet_phai_tra.SO_CON_NO, 'SO_TIEN_BU_TRU_QUY_DOI': chi_tiet_phai_tra.SO_CON_NO * ty_gia_de_nhan }]);
                                tong_tien_phai_thu = tong_tien_phai_thu - chi_tiet_phai_tra.SO_TIEN_BU_TRU
                            } else if (chi_tiet_phai_tra.SO_CON_NO > tong_tien_phai_thu) {
                                // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS': [[1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': tong_tien_phai_thu, 'SO_TIEN_BU_TRU_QUY_DOI': tong_tien_phai_thu * ty_gia_de_nhan }]] });
                                update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS'].push([1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': tong_tien_phai_thu, 'SO_TIEN_BU_TRU_QUY_DOI': tong_tien_phai_thu * ty_gia_de_nhan }])
                                tong_tien_phai_thu = 0
                            }
                        }
                    }
                } else if (tong_tien_phai_tra < tong_tien_phai_thu) {
                    for (var i in chung_tu_phai_tra) {
                        chi_tiet_phai_tra = chung_tu_phai_tra[i];
                        if (chi_tiet_phai_tra.TY_GIA_DANH_GIA_LAI > 0) {
                            ty_gia_de_nhan = chi_tiet_phai_tra.TY_GIA_DANH_GIA_LAI
                        } else {
                            ty_gia_de_nhan = chi_tiet_phai_tra.TY_GIA
                        };
                        if (chi_tiet_phai_tra.AUTO_SELECT == true) {
                            // self.updateUI({'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS': [[1, chi_tiet_phai_tra.res_id, {'SO_TIEN_BU_TRU': chi_tiet_phai_tra.SO_CON_NO,'SO_TIEN_BU_TRU_QUY_DOI': chi_tiet_phai_tra.SO_CON_NO * ty_gia_de_nhan}]] });
                            update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS'].push([1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': chi_tiet_phai_tra.SO_CON_NO, 'SO_TIEN_BU_TRU_QUY_DOI': chi_tiet_phai_tra.SO_CON_NO * ty_gia_de_nhan }]);
                        }
                        else if (chi_tiet_phai_tra.AUTO_SELECT === false) {
                            // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS': [[1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]] });
                            update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS'].push([1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]);
                        }
                    }
                    for (var i in chung_tu_phai_thu) {
                        chi_tiet_phai_thu = chung_tu_phai_thu[i];
                        if (chi_tiet_phai_thu.TY_GIA_DANH_GIA_LAI > 0) {
                            ty_gia_de_nhan = chi_tiet_phai_thu.TY_GIA_DANH_GIA_LAI
                        } else {
                            ty_gia_de_nhan = chi_tiet_phai_thu.TY_GIA
                        };
                        if (chi_tiet_phai_thu.AUTO_SELECT == true) {
                            if (tong_tien_phai_tra == 0) {
                                // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS': [[1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]] });
                                update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'].push([1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]);
                            } else if (tong_tien_phai_tra > chi_tiet_phai_thu.SO_CHUA_THU) {
                                // self.updateUI({'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS': [[1, chi_tiet_phai_thu.res_id, {'SO_TIEN_BU_TRU': chi_tiet_phai_thu.SO_CHUA_THU,'SO_TIEN_BU_TRU_QUY_DOI': chi_tiet_phai_thu.SO_CHUA_THU * ty_gia_de_nhan}]] });
                                update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'].push([1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': chi_tiet_phai_thu.SO_CHUA_THU, 'SO_TIEN_BU_TRU_QUY_DOI': chi_tiet_phai_thu.SO_CHUA_THU * ty_gia_de_nhan }])
                                tong_tien_phai_tra = tong_tien_phai_tra - chi_tiet_phai_thu.SO_TIEN_BU_TRU
                            } else if (tong_tien_phai_tra < chi_tiet_phai_thu.SO_CHUA_THU) {
                                // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS': [[1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': tong_tien_phai_tra, 'SO_TIEN_BU_TRU_QUY_DOI': tong_tien_phai_tra * ty_gia_de_nhan }]] });
                                update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'].push([1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': tong_tien_phai_tra, 'SO_TIEN_BU_TRU_QUY_DOI': tong_tien_phai_tra * ty_gia_de_nhan }])
                                tong_tien_phai_tra = 0
                            }
                        }
                    }
                } else {
                    for (i in chung_tu_phai_tra) {
                        chi_tiet_phai_tra = chung_tu_phai_tra[i];
                        if (chi_tiet_phai_tra.AUTO_SELECT == true) {
                            // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS': [[1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': chi_tiet_phai_tra.SO_CON_NO }]] });
                            update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS'].push([1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': chi_tiet_phai_tra.SO_CON_NO }])
                        }
                    }
                    for (var i in chung_tu_phai_thu) {
                        chi_tiet_phai_thu = chung_tu_phai_thu[i];
                        if (chi_tiet_phai_thu.AUTO_SELECT == true) {
                            // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS': [[1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': chi_tiet_phai_thu.SO_CHUA_THU }]] });
                            update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'].push([1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': chi_tiet_phai_thu.SO_CHUA_THU }])
                        }
                    }
                }

            }
            // TH chỉ tích CT phải thu
            else if (tong_tien_phai_thu > 0) {
                // Cập nhật lại CT phải thu và reset chứng từ phải trả
                for (var i in chung_tu_phai_thu) {
                    chi_tiet_phai_thu = chung_tu_phai_thu[i];
                    if (chi_tiet_phai_thu.TY_GIA_DANH_GIA_LAI > 0) {
                        ty_gia_de_nhan = chi_tiet_phai_thu.TY_GIA_DANH_GIA_LAI
                    } else {
                        ty_gia_de_nhan = chi_tiet_phai_thu.TY_GIA
                    };
                    if (chi_tiet_phai_thu.AUTO_SELECT == true) {
                        // self.updateUI({'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS': [[1, chi_tiet_phai_thu.res_id, {'SO_TIEN_BU_TRU': chi_tiet_phai_thu.SO_CHUA_THU, 'SO_TIEN_BU_TRU_QUY_DOI': chi_tiet_phai_thu.SO_CHUA_THU * ty_gia_de_nhan, }]] });
                        update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'].push([1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': chi_tiet_phai_thu.SO_CHUA_THU, 'SO_TIEN_BU_TRU_QUY_DOI': chi_tiet_phai_thu.SO_CHUA_THU * ty_gia_de_nhan, }]);
                    } else if (chi_tiet_phai_thu.AUTO_SELECT == false) {
                        // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS': [[1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]] });
                        update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'].push([1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]);
                    }
                };

                for (var i in chung_tu_phai_tra) {
                    chi_tiet_phai_tra = chung_tu_phai_tra[i];
                    // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS': [[1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]] });
                    update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS'].push([1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]);
                }

            }
            // TH chỉ tích CT phải thu
            else if (tong_tien_phai_tra > 0) {
                // Cập nhật lại CT phải trả và reset chứng từ phải thu
                for (var i in chung_tu_phai_tra) {
                    chi_tiet_phai_tra = chung_tu_phai_tra[i];
                    if (chi_tiet_phai_tra.TY_GIA_DANH_GIA_LAI > 0) {
                        ty_gia_de_nhan = chi_tiet_phai_tra.TY_GIA_DANH_GIA_LAI
                    } else {
                        ty_gia_de_nhan = chi_tiet_phai_tra.TY_GIA
                    };
                    if (chi_tiet_phai_tra.AUTO_SELECT == true) {
                        // self.updateUI({'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS': [[1, chi_tiet_phai_tra.res_id, {'SO_TIEN_BU_TRU': chi_tiet_phai_tra.SO_CON_NO,'SO_TIEN_BU_TRU_QUY_DOI': chi_tiet_phai_tra.SO_CON_NO * ty_gia_de_nhan,}]] });
                        update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS'].push([1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': chi_tiet_phai_tra.SO_CON_NO, 'SO_TIEN_BU_TRU_QUY_DOI': chi_tiet_phai_tra.SO_CON_NO * ty_gia_de_nhan, }]);
                    }
                    else if (chi_tiet_phai_tra.AUTO_SELECT == false) {
                        // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS': [[1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]] });
                        update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS'].push([1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]);
                    }
                };
                for (var i in chung_tu_phai_thu) {
                    chi_tiet_phai_thu = chung_tu_phai_thu[i];
                    // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS': [[1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]] });
                    update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'].push([1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]);
                }

            }
            // Bỏ tích tất cả
            else {
                for (var i in chung_tu_phai_thu) {
                    chi_tiet_phai_thu = chung_tu_phai_thu[i];
                    // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS': [[1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]] });
                    update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_THU_IDS'].push([1, chi_tiet_phai_thu.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]);
                };

                for (var i in chung_tu_phai_tra) {
                    chi_tiet_phai_tra = chung_tu_phai_tra[i];
                    // self.updateUI({ 'SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS': [[1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]] });
                    update_list['SALE_EX_BU_TRU_CONG_NO_CHUNG_TU_PHAI_TRA_IDS'].push([1, chi_tiet_phai_tra.res_id, { 'SO_TIEN_BU_TRU': 0, 'SO_TIEN_BU_TRU_QUY_DOI': 0 }]);
                }
            }
            this.updateUI(update_list);
            // Tính tổng tiền quy đổi
            if (this.getFieldValue('currency_id').display_name != 'VND') {
                if (chung_tu_phai_tra.length > 0) {
                    for (var i in chung_tu_phai_tra) {
                        if (i > 0) {
                            if (chung_tu_phai_tra[i][2].AUTO_SELECT == true) {
                                tong_tien_bu_tru_phai_tra_quy_doi += chung_tu_phai_tra[i][2].SO_TIEN_BU_TRU_QUY_DOI
                            }
                        }
                    }
                }
                if (chung_tu_phai_thu.length > 0) {
                    for (var i in chung_tu_phai_thu) {
                        if (i > 0) {
                            if (chung_tu_phai_thu[i][2].AUTO_SELECT == true) {
                                tong_tien_bu_tru_phai_thu_quy_doi += chung_tu_phai_thu[i][2].SO_TIEN_BU_TRU_QUY_DOI
                            }
                        }
                    }
                }


                // Cập nhật số tiền và tài khoản xử lý chênh lệch
                var chenh_lech_bu_tru_quy_doi = tong_tien_bu_tru_phai_tra_quy_doi - tong_tien_bu_tru_phai_thu_quy_doi;
                this.updateUI({ 'CHENH_LECH_BU_TRU_QUY_DOI': chenh_lech_bu_tru_quy_doi });
                if (chenh_lech_bu_tru_quy_doi > 0) {
                    this.rpc_action({
                        model: 'sale.ex.bu.tru.cong.no',
                        method: 'lay_tai_khoan_xu_ly',
                        callback: function (result) {
                            if (result) {
                                self.updateUI({ 'TK_XU_LY_ID': { id: result.tai_khoan_xu_ly_lai[0], display_name: result.tai_khoan_xu_ly_lai[1] } });
                            }
                        }
                    });
                } else {
                    this.rpc_action({
                        model: 'sale.ex.bu.tru.cong.no',
                        method: 'lay_tai_khoan_xu_ly',
                        callback: function (result) {
                            if (result) {
                                self.updateUI({ 'TK_XU_LY_ID': { id: result.tai_khoan_xu_ly_lo[0], display_name: result.tai_khoan_xu_ly_lo[1] } });
                            }
                        }
                    });
                }
            }
        },


    });

    var BuTruCongNoFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BuTruCongNoController,
        }),
    });

    view_registry.add('bu_tru_cong_no_form_view', BuTruCongNoFormView);

    return BuTruCongNoFormView;
});
