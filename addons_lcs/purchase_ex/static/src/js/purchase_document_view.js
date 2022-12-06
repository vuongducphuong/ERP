odoo.define('purchase_ex.purchase_document_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');


    var PurchaseDocumentController = FormController.extend({

        _onButtonClicked: function (event) {
            var self = this;
            var def = $.Deferred();
            var error = [];
            event.stopPropagation();
            switch (event.data.attrs.id) {
                case "btn_chon":
                    var arr_chung_tu_da_chon = [];
                    var arr_tham_so = [];
                    if(self.getFieldValue('CHI_PHI_IDS').length > 0){
                         var chi_phi_ids = self.getFieldValue('CHI_PHI_IDS');
                         for(var i in chi_phi_ids){
                              if(arr_chung_tu_da_chon.includes({'ID_CHUNG_TU_GOC' : chi_phi_ids[i].ID_CHUNG_TU_GOC,'SO_PHAN_BO_LAN_NAY' : chi_phi_ids[i].SO_PHAN_BO_LAN_NAY}) == false){
                                   arr_chung_tu_da_chon.push({'ID_CHUNG_TU_GOC' : chi_phi_ids[i].ID_CHUNG_TU_GOC,'SO_PHAN_BO_LAN_NAY' : chi_phi_ids[i].SO_PHAN_BO_LAN_NAY})
                              }
                         }
                    };
                    if(self.getFieldValue('PHI_TRUOC_HAI_QUAN_IDS').length > 0){
                         var phi_truoc_hai_quan_ids = self.getFieldValue('PHI_TRUOC_HAI_QUAN_IDS');
                         for(var i in phi_truoc_hai_quan_ids){
                              if(arr_chung_tu_da_chon.includes({'ID_CHUNG_TU_GOC' : phi_truoc_hai_quan_ids[i].ID_CHUNG_TU_GOC,'SO_PHAN_BO_LAN_NAY' : phi_truoc_hai_quan_ids[i].SO_PHAN_BO_LAN_NAY}) == false){
                                   arr_chung_tu_da_chon.push({'ID_CHUNG_TU_GOC' : phi_truoc_hai_quan_ids[i].ID_CHUNG_TU_GOC,'SO_PHAN_BO_LAN_NAY' : phi_truoc_hai_quan_ids[i].SO_PHAN_BO_LAN_NAY})
                              }
                         }
                    };
                    if(self.getFieldValue('PHI_HANG_VE_KHO_IDS').length > 0){
                         var phi_hang_ve_kho_ids = self.getFieldValue('PHI_HANG_VE_KHO_IDS');
                         for(var i in phi_hang_ve_kho_ids){
                              if(arr_chung_tu_da_chon.includes({'ID_CHUNG_TU_GOC' : phi_hang_ve_kho_ids[i].ID_CHUNG_TU_GOC,'SO_PHAN_BO_LAN_NAY' : phi_hang_ve_kho_ids[i].SO_PHAN_BO_LAN_NAY}) == false){
                                   arr_chung_tu_da_chon.push({'ID_CHUNG_TU_GOC' : phi_hang_ve_kho_ids[i].ID_CHUNG_TU_GOC,'SO_PHAN_BO_LAN_NAY' : phi_hang_ve_kho_ids[i].SO_PHAN_BO_LAN_NAY})
                              }
                         }
                    }
                    var id_chung_tu = event.data.record.id;
                    arr_tham_so.push(id_chung_tu);
                    arr_tham_so.push(arr_chung_tu_da_chon);
                    new dialogs.FormViewDialog(this, {
                        tham_so: arr_tham_so,
                        readonly: false,
                        res_model: 'purchase.ex.chon.chung.tu.chi.phi',
                        ref_views: [['purchase_ex.view_purchase_ex_chon_chung_tu_chi_phi_form', 'form']],
                        title: ("Chọn chứng từ chi phí"),
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        on_after_saved: function (record, changed) {
                            if (changed) {
                                if (record.data.PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS.data.length > 0) {
                                    var arr_chung_tu_chi_phi = [[5]];
                                    for (var i in record.data.PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS.data) {
                                        var chi_tiet = record.data.PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS.data[i].data;
                                        if (chi_tiet.AUTO_SELECT == true) {
                                            arr_chung_tu_chi_phi.push([0, 0, {
                                                'NGAY_HACH_TOAN': chi_tiet.NGAY_HACH_TOAN,
                                                'NGAY_CHUNG_TU': chi_tiet.NGAY_CHUNG_TU,
                                                'DOI_TUONG_ID': [chi_tiet.DOI_TUONG_ID.data.id, chi_tiet.DOI_TUONG_ID.data.display_name],
                                                'TONG_CHI_PHI': chi_tiet.TONG_CHI_PHI,
                                                'SO_PHAN_BO_LAN_NAY': chi_tiet.SO_PHAN_BO_LAN_NAY,
                                                'LUY_KE_DA_PHAN_BO': chi_tiet.LUY_KE_SO_DA_PHAN_BO,
                                                'SO_CHUNG_TU': chi_tiet.SO_CHUNG_TU,
                                                'ID_CHUNG_TU_GOC': chi_tiet.ID_CHUNG_TU_GOC,
                                            }])
                                        }

                                    }
                                }
                                self.updateUI({ 'CHI_PHI_IDS': arr_chung_tu_chi_phi });
                                $('#btn_loai_bo_chi_phi').attr('disabled', false);
                                $('#btn_phan_bo_cp').attr('disabled', false);
                            }
                        },
                    }).open();
                    break;

                case "btn_chon_truoc_hai_quan":
                    var id_chung_tu = event.data.record.id;
                    new dialogs.FormViewDialog(this, {
                        tham_so: id_chung_tu,
                        readonly: false,
                        res_model: 'purchase.ex.chon.chung.tu.chi.phi',
                        ref_views: [['purchase_ex.view_purchase_ex_chon_chung_tu_chi_phi_form', 'form']],
                        title: ("Chọn chứng từ chi phí"),
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        on_after_saved: function (record, changed) {
                            if (changed) {
                                if (record.data.PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS.data.length > 0) {
                                    var arr_chung_tu_chi_phi = [[5]];
                                    for (var i in record.data.PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS.data) {
                                        var chi_tiet = record.data.PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS.data[i].data;
                                        if (chi_tiet.AUTO_SELECT == true) {
                                            arr_chung_tu_chi_phi.push([0, 0, {
                                                'NGAY_HACH_TOAN': chi_tiet.NGAY_HACH_TOAN,
                                                'NGAY_CHUNG_TU': chi_tiet.NGAY_CHUNG_TU,
                                                'DOI_TUONG_ID': [chi_tiet.DOI_TUONG_ID.data.id, chi_tiet.DOI_TUONG_ID.data.display_name],
                                                'TONG_CHI_PHI': chi_tiet.TONG_CHI_PHI,
                                                'SO_PHAN_BO_LAN_NAY': chi_tiet.SO_PHAN_BO_LAN_NAY,
                                                'LUY_KE_DA_PHAN_BO': chi_tiet.LUY_KE_SO_DA_PHAN_BO,
                                                'SO_CHUNG_TU': chi_tiet.SO_CHUNG_TU,
                                                'ID_CHUNG_TU_GOC': chi_tiet.ID_CHUNG_TU_GOC,
                                            }])
                                        }

                                    }
                                }
                                self.updateUI({ 'PHI_TRUOC_HAI_QUAN_IDS': arr_chung_tu_chi_phi });
                                $('#btn_loai_bo_phi_truoc_hai_quan').attr('disabled', false);
                                $('#btn_phan_bo_cp_phi_truoc_hai_quan').attr('disabled', false);
                            }
                        },
                    }).open();
                    break;

                case "btn_chon_hang_ve_kho":
                    var id_chung_tu = event.data.record.id;
                    new dialogs.FormViewDialog(this, {
                        tham_so: id_chung_tu,
                        readonly: false,
                        res_model: 'purchase.ex.chon.chung.tu.chi.phi',
                        ref_views: [['purchase_ex.view_purchase_ex_chon_chung_tu_chi_phi_form', 'form']],
                        title: ("Chọn chứng từ chi phí"),
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        on_after_saved: function (record, changed) {
                            if (changed) {
                                if (record.data.PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS.data.length > 0) {
                                    var arr_chung_tu_chi_phi = [[5]];
                                    for (var i in record.data.PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS.data) {
                                        var chi_tiet = record.data.PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS.data[i].data;
                                        if (chi_tiet.AUTO_SELECT == true) {
                                            arr_chung_tu_chi_phi.push([0, 0, {
                                                'NGAY_HACH_TOAN': chi_tiet.NGAY_HACH_TOAN,
                                                'NGAY_CHUNG_TU': chi_tiet.NGAY_CHUNG_TU,
                                                'DOI_TUONG_ID': [chi_tiet.DOI_TUONG_ID.data.id, chi_tiet.DOI_TUONG_ID.data.display_name],
                                                'TONG_CHI_PHI': chi_tiet.TONG_CHI_PHI,
                                                'SO_PHAN_BO_LAN_NAY': chi_tiet.SO_PHAN_BO_LAN_NAY,
                                                'LUY_KE_DA_PHAN_BO': chi_tiet.LUY_KE_SO_DA_PHAN_BO,
                                                'SO_CHUNG_TU': chi_tiet.SO_CHUNG_TU,
                                                'ID_CHUNG_TU_GOC': chi_tiet.ID_CHUNG_TU_GOC,
                                            }])
                                        }

                                    }
                                }
                                self.updateUI({ 'PHI_HANG_VE_KHO_IDS': arr_chung_tu_chi_phi });
                                $('#btn_loai_bo_phi_hang_ve_kho').attr('disabled', false);
                                $('#btn_phan_bo_cp_phi_hang_ve_kho').attr('disabled', false);
                            }
                        },
                    }).open();
                    break;

                case "btn_chon_cpmh":
                    var id_chung_tu = event.data.record.id;
                    new dialogs.FormViewDialog(this, {
                        tham_so: id_chung_tu,
                        readonly: false,
                        res_model: 'purchase.ex.chon.chung.tu.chi.phi',
                        ref_views: [['purchase_ex.view_purchase_ex_chon_chung_tu_chi_phi_form', 'form']],
                        title: ("Chọn chứng từ chi phí"),
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        on_after_saved: function (record, changed) {
                            if (changed) {
                                if (record.data.PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS.data.length > 0) {
                                    var arr_chung_tu_chi_phi = [[5]];
                                    for (var i in record.data.PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS.data) {
                                        var chi_tiet = record.data.PURCHASE_EX_CHON_CHUNG_TU_CHI_PHI_CHI_TIET_IDS.data[i].data;
                                        if (chi_tiet.AUTO_SELECT == true) {
                                            arr_chung_tu_chi_phi.push([0, 0, {
                                                'NGAY_HACH_TOAN': chi_tiet.NGAY_HACH_TOAN,
                                                'NGAY_CHUNG_TU': chi_tiet.NGAY_CHUNG_TU,
                                                'DOI_TUONG_ID': [chi_tiet.DOI_TUONG_ID.data.id, chi_tiet.DOI_TUONG_ID.data.display_name],
                                                'TONG_CHI_PHI': chi_tiet.TONG_CHI_PHI,
                                                'SO_PHAN_BO_LAN_NAY': chi_tiet.SO_PHAN_BO_LAN_NAY,
                                                'LUY_KE_DA_PHAN_BO': chi_tiet.LUY_KE_SO_DA_PHAN_BO,
                                                'SO_CHUNG_TU': chi_tiet.SO_CHUNG_TU,
                                                'ID_CHUNG_TU_GOC': chi_tiet.ID_CHUNG_TU_GOC,
                                            }])
                                        }

                                    }
                                }
                                self.updateUI({ 'CHI_PHI_MUA_HANG_IDS': arr_chung_tu_chi_phi });
                                $('#btn_loai_bo_chi_phi_mua_hang').attr('disabled', false);
                                $('#btn_phan_bo_cp_chi_phi_mua_hang').attr('disabled', false);
                            }
                        },
                    }).open();
                    break;
                // Nút loại bỏ của tab chi phí
                case "btn_loai_bo_chi_phi":
                    var arr_rong = [[5]];
                    self.updateUI({ 'CHI_PHI_IDS': arr_rong });
                    $('#btn_phan_bo_cp').attr('disabled', true);
                    break;
                // nút loại bỏ phí trước hải quan
                case "btn_loai_bo_phi_truoc_hai_quan":
                    var arr_rong = [[5]];
                    self.updateUI({ 'PHI_TRUOC_HAI_QUAN_IDS': arr_rong });
                    $('#btn_phan_bo_cp_phi_truoc_hai_quan').attr('disabled', true);
                    break;
                // nút loại bỏ phí hàng về kho
                case "btn_loai_bo_phi_hang_ve_kho":
                    var arr_rong = [[5]];
                    self.updateUI({ 'CHI_PHI_IDS': arr_rong });
                    $('#btn_phan_bo_cp_phi_hang_ve_kho').attr('disabled', true);
                    break;
                // nút loại bỏ chi phí mua hàng
                case "btn_loai_bo_chi_phi_mua_hang":
                    var arr_rong = [[5]];
                    self.updateUI({ 'CHI_PHI_IDS': arr_rong });
                    $('#btn_phan_bo_cp_chi_phi_mua_hang').attr('disabled', true);
                    break;

                // Nút phân bổ chi phí của tab chi phí
                case "btn_phan_bo_cp":
                    var du_lieu = this.getFieldValue('CHI_TIET_IDS');
                    var chi_tiet_phan_bo = this.getFieldValue('CHI_PHI_IDS');
                    var arr_chung_tu_mua_hang_chi_tiet = [[5]];
                    var arr_tham_so = [];
                    var tong_chi_phi_mua_hang = 0;
                    var tong_thanh_tien = 0;
                    for (var i in du_lieu) {
                        var chi_tiet = du_lieu[i];
                        tong_thanh_tien += chi_tiet.THANH_TIEN;
                        arr_chung_tu_mua_hang_chi_tiet.push([0, 0, {
                            'MA_HANG_ID': [chi_tiet.MA_HANG_ID.id, chi_tiet.MA_HANG_ID.display_name],
                            'TEN_HANG': chi_tiet.name,
                            'SO_LUONG': chi_tiet.SO_LUONG,
                            'THANH_TIEN': chi_tiet.THANH_TIEN,
                            'TY_LE_PHAN_BO': 0,
                            'CHI_PHI_MUA_HANG': 0,
                        }]);
                    }
                    for (var i in chi_tiet_phan_bo) {
                        tong_chi_phi_mua_hang += chi_tiet_phan_bo[i].SO_PHAN_BO_LAN_NAY;
                    }
                    arr_tham_so.push(tong_thanh_tien);
                    arr_tham_so.push(arr_chung_tu_mua_hang_chi_tiet);
                    arr_tham_so.push(tong_chi_phi_mua_hang);

                    new dialogs.FormViewDialog(this, {
                        tham_so: arr_tham_so,
                        model: this.model,
                        res_model: this.modelName,
                        parent_form: self,
                        recordID: this.handle,
                        res_id: this.res_id,
                        ref_views: [['purchase_ex.view_purchase_ex_phan_bo_chi_phi_mua_hang_tham_so_form', 'form']],
                        title: ("Phân bổ chi phí mua hàng"),
                        readonly: false,
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        on_after_saved: function (record, changed) { // dict_record vaf arr_changed
                            if (changed) {
                                var tong_tien_phan_bo_chi_phi = 0;
                                var phan_bo_chi_chi_chi_tiet = record.data.PHAN_BO_CHI_PHI_MUA_HANG_IDS.data;
                                for (var i in phan_bo_chi_chi_chi_tiet) {
                                    tong_tien_phan_bo_chi_phi += phan_bo_chi_chi_chi_tiet[i].data.CHI_PHI_MUA_HANG;
                                }
                                if (tong_tien_phan_bo_chi_phi != record.data.TONG_CHI_PHI_MUA_HANG) {
                                    error = 'Tổng <Chi phí mua hàng> Phân bổ cho các mặt hàng phải bằng <Tổng chi phí mua hàng>';
                                }
                                else {
                                    for (var i in du_lieu) {
                                        for (var j in phan_bo_chi_chi_chi_tiet) {
                                            var chi_tiet_pb_chi_phi = phan_bo_chi_chi_chi_tiet[j];
                                            if (du_lieu[i].MA_HANG_ID.id == chi_tiet_pb_chi_phi.data.MA_HANG_ID.data.id.id) {
                                                self.updateUI({'CHI_TIET_IDS': [[1,du_lieu[i].res_id,{'CHI_PHI_MUA_HANG':chi_tiet_pb_chi_phi.data.CHI_PHI_MUA_HANG}]]});
                                            }
                                        }
                                    }
                                    for (var i in chi_tiet_phan_bo) {
                                        var chi_phi = chi_tiet_phan_bo[i];
                                        if(chi_phi.TONG_CHI_PHI < tong_tien_phan_bo_chi_phi){
                                            self.updateUI({'CHI_PHI_IDS': [[1,chi_phi.res_id,{'LUY_KE_DA_PHAN_BO':chi_phi.TONG_CHI_PHI}]]});
                                            tong_tien_phan_bo_chi_phi -= chi_phi.TONG_CHI_PHI;
                                        }
                                        else{
                                            self.updateUI({'CHI_PHI_IDS': [[1,chi_phi.res_id,{'LUY_KE_DA_PHAN_BO':tong_tien_phan_bo_chi_phi}]]});
                                        }
                                    }
                                }
                                if (error.length) {
                                    Dialog.show_message('Thông báo', error, 'ALERT')
                                    .then(function(result) {
                                        // Xử lý sau khi đóng popup
                                    });
                                    def.resolve(false);
                                } else {
                                    def.resolve(true);
                                }
                                return def;
                            }

                        },
                    }).open();
                    break;
                // Nút Phân bổ chi phí của phí trước hải quan
                case "btn_phan_bo_cp_phi_truoc_hai_quan":
                    var du_lieu = this.getFieldValue('CHI_TIET_IDS');
                    var chi_tiet_phan_bo = this.getFieldValue('PHI_TRUOC_HAI_QUAN_IDS');
                    var arr_chung_tu_mua_hang_chi_tiet = [[5]];
                    var arr_tham_so = [];
                    var tong_chi_phi_mua_hang = 0;
                    var tong_thanh_tien = 0;
                    for (var i in du_lieu) {
                        var chi_tiet = du_lieu[i];
                        tong_thanh_tien += chi_tiet.THANH_TIEN;
                        arr_chung_tu_mua_hang_chi_tiet.push([0, 0, {
                            'MA_HANG_ID': [chi_tiet.MA_HANG_ID.id.id, chi_tiet.MA_HANG_ID.id.display_name],
                            'TEN_HANG': chi_tiet.name,
                            'SO_LUONG': chi_tiet.SO_LUONG,
                            'THANH_TIEN': chi_tiet.THANH_TIEN,
                            'TY_LE_PHAN_BO': 0,
                            'CHI_PHI_MUA_HANG': 0,
                        }]);
                    }
                    for (var i in chi_tiet_phan_bo) {
                        tong_chi_phi_mua_hang += chi_tiet_phan_bo[i].SO_PHAN_BO_LAN_NAY;
                    }
                    arr_tham_so.push(tong_thanh_tien);
                    arr_tham_so.push(arr_chung_tu_mua_hang_chi_tiet);
                    arr_tham_so.push(tong_chi_phi_mua_hang);

                    new dialogs.FormViewDialog(this, {
                        tham_so: arr_tham_so,
                        model: this.model,
                        res_model: this.modelName,
                        parent_form: self,
                        recordID: this.handle,
                        res_id: this.res_id,
                        ref_views: [['purchase_ex.view_purchase_ex_bo_doi_tru_tham_so_form', 'form']],
                        title: ("Phân bổ chi phí mua hàng"),
                        readonly: false,
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        on_after_saved: function (record, changed) { // dict_record vaf arr_changed
                            if (changed) {
                                var tong_tien_phan_bo_chi_phi = 0;
                                var phan_bo_chi_chi_chi_tiet = record.data.PHAN_BO_CHI_PHI_MUA_HANG_IDS.data;
                                for (var i in phan_bo_chi_chi_chi_tiet) {
                                    tong_tien_phan_bo_chi_phi += phan_bo_chi_chi_chi_tiet[i].data.CHI_PHI_MUA_HANG;
                                }
                                if (tong_tien_phan_bo_chi_phi != record.data.TONG_CHI_PHI_MUA_HANG) {
                                    error = 'Tổng <Chi phí mua hàng> Phân bổ cho các mặt hàng phải bằng <Tổng chi phí mua hàng>';
                                }
                                else {
                                    var dict_don_mua_hang_chi_tiet_moi = [[5]];
                                    for (var i in du_lieu) {
                                        for (var j in phan_bo_chi_chi_chi_tiet) {
                                            var chi_tiet_mua_hang = du_lieu[i];
                                            var chi_tiet_pb_chi_phi = phan_bo_chi_chi_chi_tiet[j];
                                            if (chi_tiet_mua_hang.MA_HANG_ID.id == chi_tiet_pb_chi_phi.data.MA_HANG_ID.data.id.id) {
                                                _.extend(chi_tiet_mua_hang, { 'CHI_PHI_MUA_HANG': chi_tiet_pb_chi_phi.data.CHI_PHI_MUA_HANG });
                                                dict_don_mua_hang_chi_tiet_moi.push([0, 0, chi_tiet_mua_hang])
                                            }
                                        }
                                    }
                                    self.updateUI({ 'CHI_TIET_IDS': dict_don_mua_hang_chi_tiet_moi });
                                }
                                if (error.length) {
                                    self.notifyInvalidFields(error);
                                    def.resolve(false);
                                } else {
                                    def.resolve(true);
                                }
                                return def;
                            }

                        },
                    }).open();
                    break;
                // Nút phân bổ chi phí của Phi hàng về kho
                case "btn_phan_bo_cp_phi_hang_ve_kho":
                    var du_lieu = this.getFieldValue('CHI_TIET_IDS');
                    var chi_tiet_phan_bo = this.getFieldValue('CHI_PHI_IDS');
                    var arr_chung_tu_mua_hang_chi_tiet = [[5]];
                    var arr_tham_so = [];
                    var tong_chi_phi_mua_hang = 0;
                    var tong_thanh_tien = 0;
                    for (var i in du_lieu) {
                        var chi_tiet = du_lieu[i];
                        tong_thanh_tien += chi_tiet.THANH_TIEN;
                        arr_chung_tu_mua_hang_chi_tiet.push([0, 0, {
                            'MA_HANG_ID': [chi_tiet.MA_HANG_ID.id.id, chi_tiet.MA_HANG_ID.id.display_name],
                            'TEN_HANG': chi_tiet.name,
                            'SO_LUONG': chi_tiet.SO_LUONG,
                            'THANH_TIEN': chi_tiet.THANH_TIEN,
                            'TY_LE_PHAN_BO': 0,
                            'CHI_PHI_MUA_HANG': 0,
                        }]);
                    }
                    for (var i in chi_tiet_phan_bo) {
                        tong_chi_phi_mua_hang += chi_tiet_phan_bo[i].SO_PHAN_BO_LAN_NAY;
                    }
                    arr_tham_so.push(tong_thanh_tien);
                    arr_tham_so.push(arr_chung_tu_mua_hang_chi_tiet);
                    arr_tham_so.push(tong_chi_phi_mua_hang);

                    new dialogs.FormViewDialog(this, {
                        tham_so: arr_tham_so,
                        model: this.model,
                        res_model: this.modelName,
                        parent_form: self,
                        recordID: this.handle,
                        res_id: this.res_id,
                        ref_views: [['purchase_ex.view_purchase_ex_bo_doi_tru_tham_so_form', 'form']],
                        title: ("Phân bổ chi phí mua hàng"),
                        readonly: false,
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        on_after_saved: function (record, changed) { // dict_record vaf arr_changed
                            if (changed) {
                                var tong_tien_phan_bo_chi_phi = 0;
                                var phan_bo_chi_chi_chi_tiet = record.data.PHAN_BO_CHI_PHI_MUA_HANG_IDS.data;
                                for (var i in phan_bo_chi_chi_chi_tiet) {
                                    tong_tien_phan_bo_chi_phi += phan_bo_chi_chi_chi_tiet[i].data.CHI_PHI_MUA_HANG;
                                }
                                if (tong_tien_phan_bo_chi_phi != record.data.TONG_CHI_PHI_MUA_HANG) {
                                    error = 'Tổng <Chi phí mua hàng> Phân bổ cho các mặt hàng phải bằng <Tổng chi phí mua hàng>';
                                }
                                else {
                                    var dict_don_mua_hang_chi_tiet_moi = [[5]];
                                    for (var i in du_lieu) {
                                        for (var j in phan_bo_chi_chi_chi_tiet) {
                                            var chi_tiet_mua_hang = du_lieu[i];
                                            var chi_tiet_pb_chi_phi = phan_bo_chi_chi_chi_tiet[j];
                                            if (chi_tiet_mua_hang.MA_HANG_ID.id == chi_tiet_pb_chi_phi.data.MA_HANG_ID.data.id.id) {
                                                _.extend(chi_tiet_mua_hang, { 'CHI_PHI_MUA_HANG': chi_tiet_pb_chi_phi.data.CHI_PHI_MUA_HANG });
                                                dict_don_mua_hang_chi_tiet_moi.push([0, 0, chi_tiet_mua_hang])
                                            }
                                        }
                                    }
                                    self.updateUI({ 'CHI_TIET_IDS': dict_don_mua_hang_chi_tiet_moi });
                                }
                                if (error.length) {
                                    self.notifyInvalidFields(error);
                                    def.resolve(false);
                                } else {
                                    def.resolve(true);
                                }
                                return def;
                            }

                        },
                    }).open();
                    break;
                // Nút phân bổ chi phí của Chi phí mua hàng
                case "btn_phan_bo_cp_chi_phi_mua_hang":
                    var du_lieu = this.getFieldValue('CHI_TIET_IDS');
                    var chi_tiet_phan_bo = this.getFieldValue('CHI_PHI_IDS');
                    var arr_chung_tu_mua_hang_chi_tiet = [[5]];
                    var arr_tham_so = [];
                    var tong_chi_phi_mua_hang = 0;
                    var tong_thanh_tien = 0;
                    for (var i in du_lieu) {
                        var chi_tiet = du_lieu[i];
                        tong_thanh_tien += chi_tiet.THANH_TIEN;
                        arr_chung_tu_mua_hang_chi_tiet.push([0, 0, {
                            'MA_HANG_ID': [chi_tiet.MA_HANG_ID.id.id, chi_tiet.MA_HANG_ID.id.display_name],
                            'TEN_HANG': chi_tiet.name,
                            'SO_LUONG': chi_tiet.SO_LUONG,
                            'THANH_TIEN': chi_tiet.THANH_TIEN,
                            'TY_LE_PHAN_BO': 0,
                            'CHI_PHI_MUA_HANG': 0,
                        }]);
                    }
                    for (var i in chi_tiet_phan_bo) {
                        tong_chi_phi_mua_hang += chi_tiet_phan_bo[i].SO_PHAN_BO_LAN_NAY;
                    }
                    arr_tham_so.push(tong_thanh_tien);
                    arr_tham_so.push(arr_chung_tu_mua_hang_chi_tiet);
                    arr_tham_so.push(tong_chi_phi_mua_hang);

                    new dialogs.FormViewDialog(this, {
                        tham_so: arr_tham_so,
                        model: this.model,
                        res_model: this.modelName,
                        parent_form: self,
                        recordID: this.handle,
                        res_id: this.res_id,
                        ref_views: [['purchase_ex.view_purchase_ex_bo_doi_tru_tham_so_form', 'form']],
                        title: ("Phân bổ chi phí mua hàng"),
                        readonly: false,
                        disable_multiple_selection: true,
                        shouldSaveLocally: true,
                        on_after_saved: function (record, changed) { // dict_record vaf arr_changed
                            if (changed) {
                                var tong_tien_phan_bo_chi_phi = 0;
                                var phan_bo_chi_chi_chi_tiet = record.data.PHAN_BO_CHI_PHI_MUA_HANG_IDS.data;
                                for (var i in phan_bo_chi_chi_chi_tiet) {
                                    tong_tien_phan_bo_chi_phi += phan_bo_chi_chi_chi_tiet[i].data.CHI_PHI_MUA_HANG;
                                }
                                if (tong_tien_phan_bo_chi_phi != record.data.TONG_CHI_PHI_MUA_HANG) {
                                    error = 'Tổng <Chi phí mua hàng> Phân bổ cho các mặt hàng phải bằng <Tổng chi phí mua hàng>';
                                }
                                else {
                                    var dict_don_mua_hang_chi_tiet_moi = [[5]];
                                    for (var i in du_lieu) {
                                        for (var j in phan_bo_chi_chi_chi_tiet) {
                                            var chi_tiet_mua_hang = du_lieu[i];
                                            var chi_tiet_pb_chi_phi = phan_bo_chi_chi_chi_tiet[j];
                                            if (chi_tiet_mua_hang.MA_HANG_ID.id == chi_tiet_pb_chi_phi.data.MA_HANG_ID.data.id.id) {
                                                _.extend(chi_tiet_mua_hang, { 'CHI_PHI_MUA_HANG': chi_tiet_pb_chi_phi.data.CHI_PHI_MUA_HANG });
                                                dict_don_mua_hang_chi_tiet_moi.push([0, 0, chi_tiet_mua_hang])
                                            }
                                        }
                                    }
                                    self.updateUI({ 'CHI_TIET_IDS': dict_don_mua_hang_chi_tiet_moi });
                                }
                                if (error.length) {
                                    self.notifyInvalidFields(error);
                                    def.resolve(false);
                                } else {
                                    def.resolve(true);
                                }
                                return def;
                            }

                        },
                    }).open();
                    break;

                case "btn_phan_bo_chiet_khau":
                    return new dialogs.FormParamsDialog(this, _.extend({}, this.nodeOptions, {
                        res_model: 'purchase.ex.phan.bo.chiet.khau.theo.hoa.don',
                        title: 'Phân bổ chiết khấu theo hóa đơn',
                        size:'medium',
                        ref_views: [['purchase_ex.view_purchase_ex_phan_bo_chiet_khau_theo_hoa_don_form', 'form']],
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_selected: function (records, handle) {
                            self.changeFieldValue('PHAN_BO_CHIET_KHAU_JSON', records);
                             self.closeDialog(handle);
                        },
                    })).open();
                    break;

                case "btn_lap_tu_don_mua_hang":
                    var loai_chung_tu = self.getFieldValue('LOAI_CHUNG_TU');
                    var loai_tien = self.getFieldValue('currency_id');
                    var tham_so = [];
                    tham_so.push(loai_chung_tu,loai_tien)
                    return new dialogs.FormViewDialog(self, {
                        tham_so : tham_so,
                        model: this.model,
                        readonly: this.mode == "readonly",
                        shouldSaveLocally: true,
                        disable_multiple_selection: true,
                        res_model: 'purchase.ex.lap.tu.don.mua.hang.form',
                        title: 'Chọn đơn mua hàng',
                        ref_views: [['purchase_ex.view_purchase_ex_lap_tu_don_mua_hang_form_tham_so_form', 'form']],
                        field: event.data.field,
                        on_before_saved: function(controller) {
                            var def = $.Deferred();
                            var dem = 0;
                            var chi_tiet = controller.getFieldValue('PURCHASE_EX_LAP_TU_DON_MUA_HANG_CHI_TIET_IDS');
                            for (var i= 0 ; i < chi_tiet.length; i++){
                                    if(chi_tiet[i].AUTO_SELECT){
                                            dem = dem + 1;
                                    }
                            }
                            if(dem == 0){
                                error = 'Bạn phải chọn ít nhất 1 dòng đơn mua hàng.';
                                self.notifyInvalidFields(error);
                                def.resolve(false);
                            }
                            def.resolve(true);
                            return def;

                        },
                        on_after_saved: function (record, changes) {
                            
                            if (changes) {
                                // var default_chi_tiet_so_du_ngoai_te = [[5]];
                                var current_data = record.data;
                                // var doi_tuong_id;
                                // var ma_doi_tuong;
                                // var arr_lap_tu_don_mua_hang = [];
                                var list_chi_tiet_so_luong = '';
                                var chitiet_ids = current_data.PURCHASE_EX_LAP_TU_DON_MUA_HANG_CHI_TIET_IDS.data;
                                for (var i = 0; i < chitiet_ids.length; i++) {

                                    //chỉ lấy những thằng chọn
                                    var chi_tiet = chitiet_ids[i].data;
                                    
                                    if (chi_tiet.AUTO_SELECT) {
                                        list_chi_tiet_so_luong += chi_tiet.ID_DON_MUA_HANG_CT + ',' + chi_tiet.SO_LUONG_NHAN;
                                        list_chi_tiet_so_luong += ';';
                                        // arr_lap_tu_don_mua_hang.push(chi_tiet_so_luong)
                                        // var tk_thue_gtgt_id = false;
                                        // var tk_co_id = false;
                                        // var tk_no_id = false;
                                        // var kho_id = false;
                                        // var dvt_id = false;
                                        // var don_mua_hang = false;
                                        // var don_mua_hang_chi_tiet_id = false;
                                        // var hang = false;
                                        // if(chi_tiet.DOI_TUONG_ID){
                                        //    doi_tuong_id = chi_tiet.DOI_TUONG_ID.data.id;
                                        //    ma_doi_tuong = chi_tiet.DOI_TUONG_ID.data.display_name;
                                        // };
                                        // if(chi_tiet.TK_THUE_GTGT_ID){
                                        //    tk_thue_gtgt_id = chi_tiet.TK_THUE_GTGT_ID.data.id;
                                        // };
                                        // if(chi_tiet.TK_CO_ID){
                                        //    tk_co_id = chi_tiet.TK_CO_ID.data.id;
                                        // };
                                        // if(chi_tiet.TK_NO_ID){
                                        //    tk_no_id = chi_tiet.TK_NO_ID.data.id;
                                        // };
                                        // if(chi_tiet.KHO_ID){
                                        //    kho_id = chi_tiet.KHO_ID.data.id;
                                        // };
                                        // if(chi_tiet.DVT_ID){
                                        //    dvt_id = chi_tiet.DVT_ID.data.id;
                                        // };
                                        // if(chi_tiet.DON_MUA_HANG_ID){
                                        //    don_mua_hang = chi_tiet.DON_MUA_HANG_ID.data;
                                        // };
                                        // if(chi_tiet.MA_HANG){
                                        //    hang = chi_tiet.MA_HANG.data;
                                        // };
                                        // if(chi_tiet.ID_DON_MUA_HANG_CT){
                                        //     don_mua_hang_chi_tiet_id = chi_tiet.ID_DON_MUA_HANG_CT;
                                        //  };
                                        // default_chi_tiet_so_du_ngoai_te.push([0, 0, {
                                        //     'MA_HANG_ID': [hang.id, hang.display_name],
                                        //     'name': chi_tiet.TEN_HANG,
                                        //     'DVT_ID' : dvt_id,
                                        //     'SO_LUONG': chi_tiet.SO_LUONG_NHAN,
                                        //     'DON_GIA': chi_tiet.DON_GIA,
                                        //     'THANH_TIEN': chi_tiet.THANH_TIEN,
                                        //     'GIA_TRI_NHAP_KHO': chi_tiet.THANH_TIEN,
                                        //     'DON_MUA_HANG_ID': [don_mua_hang.id, don_mua_hang.display_name],
                                        //     'KHO_ID': kho_id,
                                        //     'TK_THUE_GTGT_ID': tk_thue_gtgt_id,
                                        //     'TK_CO_ID': tk_co_id,
                                        //     'TK_NO_ID': tk_no_id,
                                        //     'CHI_TIET_DON_MUA_HANG_ID': don_mua_hang_chi_tiet_id,
                                        // }])
                                    }


                                }
                                // var lay_tu_don_mua_hang_json = JSON.stringify(arr_lap_tu_don_mua_hang);
                                self.changeFieldValue('LAP_TU_DON_MUA_HANG_JSON',list_chi_tiet_so_luong);
                                // self.updateUI({ 'CHI_TIET_IDS': default_chi_tiet_so_du_ngoai_te,
                                // 'DOI_TUONG_ID':[doi_tuong_id,ma_doi_tuong],});
                                // this.rpc_action({
                                //     model: 'account.ex.so.du.tai.khoan',
                                //     method: 'lay_so_du_tai_khoan',
                                //     callback: function(result) {
                                //         if (result) {
                                //         }
                                //     }
                                // });
                            }
                        }
                    }).open();
                    break;
                case "btn_lap_tu_lenh_san_xuat":
                    return new dialogs.FormViewDialog(self, {
                        model: this.model,
                        readonly: this.mode == "readonly",
                        shouldSaveLocally: true,
                        disable_multiple_selection: true,
                        res_model: 'purchase.ex.chon.tu.lenh.san.xuat.form',
                        title: 'Chọn lệnh sản xuất',
                        ref_views: [['purchase_ex.view_purchase_ex_chon_tu_lenh_san_xuat_form_tham_so_form', 'form']],
                        size: 'huge',
                        field: event.data.field,
                        on_before_saved: function(controller) {
                            var def = $.Deferred();
                            var dem = 0;
                            var chi_tiet = controller.getFieldValue('PURCHASE_EX_CHON_TU_LENH_SAN_XUAT_FORM_CHI_TIET_IDS');
                            for (var i= 0 ; i < chi_tiet.length; i++){
                                    if(chi_tiet[i].AUTO_SELECT){
                                            dem = dem + 1;
                                    }
                            }
                            if(dem == 0){
                                error = 'Bạn phải chọn ít nhất 1 dòng lệnh sản xuất.';
                                self.notifyInvalidFields(error);
                                def.resolve(false);
                            }
                            def.resolve(true);
                            return def;

                        },
                        on_after_saved: function (record, changes) {
                            if (changes) {
                                var default_danh_sach_chung_tu_chi_tiet = [[5]];


                                var current_data = record.data;
                                var chitiet_ids = current_data.PURCHASE_EX_CHON_TU_LENH_SAN_XUAT_FORM_CHI_TIET_IDS.data;
                                var id_thanh_pham_list = [];

                                for (var i = 0; i < chitiet_ids.length; i++) {

                                    //chỉ lấy những thằng chọn
                                    var chi_tiet = chitiet_ids[i].data;
                                    if (chi_tiet.AUTO_SELECT) {

                                        id_thanh_pham_list.push(chi_tiet.ID_THANH_PHAM);
                                    }

                                }
                                self.rpc_action({
                                    model: 'purchase.ex.chon.tu.lenh.san.xuat.form',
                                    method: 'thuc_hien_lay_chi_tiet_thanh_pham',
                                    args: { 'id_thanh_pham_list': id_thanh_pham_list, },
                                    callback: function (result) {
                                        if (result) {
                                            self.updateUI({ 'CHI_TIET_IDS': result, });
                                        }
                                    }
                                });

                            }
                        }
                    }).open();
                    break;
                case "btn_lap_tu_chung_tu_ban_hang":
                    return new dialogs.FormViewDialog(self, {
                        model: this.model,
                        readonly: this.mode == "readonly",
                        shouldSaveLocally: true,
                        disable_multiple_selection: true,
                        res_model: 'purchase.ex.lap.tu.chung.tu.ban.hang.form',
                        title: 'Chọn chứng từ bán hàng',
                        ref_views: [['purchase_ex.view_purchase_ex_lap_tu_chung_tu_ban_hang_form_tham_so_form', 'form']],
                        size: 'huge',
                        field: event.data.field,
                        on_before_saved: function(controller) {
                            var def = $.Deferred();
                            var dem = 0;
                            var chi_tiet = controller.getFieldValue('PURCHASE_EX_LAP_TU_CHUNG_TU_BAN_HANG_FORM_CHI_TIET_IDS');
                            for (var i= 0 ; i < chi_tiet.length; i++){
                                    if(chi_tiet[i].AUTO_SELECT){
                                            dem = dem + 1;
                                    }
                            }
                            if(dem == 0){
                                error = 'Bạn phải chọn ít nhất 1 dòng chứng từ bán hàng.';
                                self.notifyInvalidFields(error);
                                def.resolve(false);
                            }
                            def.resolve(true);
                            return def;

                        },
                        on_after_saved: function (record, changes) {
                            if (changes) {
                                var list_id_chung_tu_ban_hang = [];
                                var current_data = record.data;
                                var chitiet_ids = current_data.PURCHASE_EX_LAP_TU_CHUNG_TU_BAN_HANG_FORM_CHI_TIET_IDS.data;
                                for (var i = 0; i < chitiet_ids.length; i++) {

                                    //chỉ lấy những thằng chọn
                                    var chi_tiet = chitiet_ids[i].data;
                                    
                                    if (chi_tiet.AUTO_SELECT) {
                                        list_id_chung_tu_ban_hang.push(chi_tiet.ID_CHUNG_TU_BAN_HANG);
                                    }
                                }
                                self.rpc_action({
                                    model: 'purchase.ex.lap.tu.chung.tu.ban.hang.form',
                                    method: 'thuc_hien_lay_chi_tiet_cac_chung_tu',
                                    args: { 'list_id_chung_tu_ban_hang': list_id_chung_tu_ban_hang },
                                    callback: function (result) {
                                        if (result) {
                                            self.updateUI({ 'CHI_TIET_IDS': result, });
                                        }
                                    }
                                });
                            }
                        }
                    }).open();
                    break;

                // case "action_bo_ghi_so":
                ///////////////////////////////////////
                ////////////START BO_GHI_SO////////////
                ///////////////////////////////////////
                // var self = this;
                // var id_chung_tu_goc = event.data.record.data.id;
                // this.rpc_action({
                //     model: self.modelName,
                //     method: 'action_bo_ghi_so',
                //     args: {
                //         '_id' : id_chung_tu_goc,
                //     },
                //     callback: function(result) {
                //         if (result) {
                //             var tham_so = result;
                //             if(tham_so.loi == true){
                //                 if (tham_so.loai_loi == 'PB_CHI_PHI'){
                //                     var id_chung_tu_lien_quan = tham_so.id_chung_tu_lien_quan;
                //                     Dialog.show_message('tieu_de', tham_so.str_loi, 'CONFIRM')
                //                     .then(function(result) {
                //                         if(result == true) {
                //                             self.rpc_action({
                //                                 model: self.modelName,
                //                                 method: 'bo_ghi_so_cac_chung_tu_lien_quan',
                //                                 args: {
                //                                     'id_chung_tu_lien_quan' : id_chung_tu_lien_quan,
                //                                     'model_chung_tu_lien_quan' : 'purchase.document',
                //                                     '_id' : id_chung_tu_goc,
                //                                 },
                //                                 callback: function(result) {
                //                                     if(result == true){
                //                                         Dialog.show_message('', 'Bỏ ghi sổ chứng từ liên quan không thành công, bạn vui lòng kiểm tra chứng từ liên quan', 'ALERT')
                //                                     } else {
                //                                         self.reload();
                //                                     }
                //                                 }
                //                             });
                //                         }
                //                     });
                //                 } else {
                //                     Dialog.show_message('tieu_de', tham_so.str_loi, 'CONFIRM')
                //                 };
                //             } else {
                //                 self.reload();
                //             }
                //         }
                //     }
                // });
                ///////////////////////////////////////
                /////////////END BO_GHI_SO/////////////
                ///////////////////////////////////////
                // break;
                default:
                    this._super.apply(this, arguments);
            }

        },

        onViewLoaded: function (e, defer) {
            var self = this;
            var def = defer;
            this.$('#btn_loai_bo_chi_phi').attr('disabled', true);
            this.$('#btn_phan_bo_cp').attr('disabled', true);
            this.$('#btn_loai_bo_phi_truoc_hai_quan').attr('disabled', true);
            this.$('#btn_phan_bo_cp_phi_truoc_hai_quan').attr('disabled', true);
            this.$('#btn_loai_bo_phi_hang_ve_kho').attr('disabled', true);
            this.$('#btn_phan_bo_cp_phi_hang_ve_kho').attr('disabled', true);
            this.$('#btn_loai_bo_chi_phi_mua_hang').attr('disabled', true);
            this.$('#btn_phan_bo_cp_chi_phi_mua_hang').attr('disabled', true);
            this._changeChiTietSelection();
            if (def) {
                def.resolve();
            }
        },

        onFieldChanged: function (field) {
            var self = this;
            if ("LOAI_CHUNG_TU_MH" == field || "LOAI_HOA_DON" == field) {
                this._changeChiTietSelection();
            } else if ('DOI_TUONG_ID' == field) {
                var doi_tuong = this.getFieldValue('DOI_TUONG_ID')
                var doi_tuong_id = doi_tuong ? doi_tuong.id : false;
                self.getFieldWidget('TK_NHAN_ID').changeDomain([['DOI_TUONG_ID', '=', doi_tuong_id]]);
            }

        },

        _changeChiTietSelection: function() {
            var LOAI_CHUNG_TU_MH = this.getFieldValue('LOAI_CHUNG_TU_MH');
            var LOAI_HOA_DON = this.getFieldValue('LOAI_HOA_DON');
            if (LOAI_CHUNG_TU_MH == 'trong_nuoc_nhap_kho') {
                // Nhận kèm hóa đơn
                if (LOAI_HOA_DON == '1') {
                    this.changeSelectionSource('CHI_TIET_HANG_HOA', ['hang_tien', 'thue']);
                } else {
                    this.changeSelectionSource('CHI_TIET_HANG_HOA', ['hang_tien']);
                }
            }
            else if (LOAI_CHUNG_TU_MH == 'trong_nuoc_khong_qua_kho') {
                if (LOAI_HOA_DON == '1') {
                    this.changeSelectionSource('CHI_TIET_HANG_HOA');
                } else {
                    this.changeSelectionSource('CHI_TIET_HANG_HOA', ['hang_tien', 'thong_ke']);
                }
            } else if (LOAI_CHUNG_TU_MH == 'nhap_khau_nhap_kho') {
                this.changeSelectionSource('CHI_TIET_HANG_HOA', ['hang_tien', 'thue']);
            } else if (LOAI_CHUNG_TU_MH == 'nhap_khau_khong_qua_kho') {
                this.changeSelectionSource('CHI_TIET_HANG_HOA', ['hang_tien', 'thue']);
            }
        },

    });

    var PurchaseDocumentView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: PurchaseDocumentController,
        }),
    });

    view_registry.add('purchase_document_view', PurchaseDocumentView);

    return PurchaseDocumentView;
});