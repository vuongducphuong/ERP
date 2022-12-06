odoo.define('tien_luong.tien_luong_tra_luong_form_tham_so_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var TienLuongTraLuongController = FormController.extend({
        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
        },
        _onButtonClicked: function (event) {
            var self = this;
            event.stopPropagation();
            var def = $.Deferred();
            var error = [];
            switch (event.data.attrs.id) {
                case "btn_tra_luong":
                    var record = event.data.record.data;
                    var param = {};
                    var ref_views = [];
                    var title;
                    var list_nhan_vien = record.TIEN_LUONG_TRA_LUONG_FORM_THAM_SO_CHI_TIET_IDS.data;
                    var ngay_tra_luong = self.getFieldValue('NGAY_TRA_LUONG');
                    var arr_list_thong_tin_tra_luong_nhan_vien = [];
                    var so_tien_hach_toan = 0;
                    var dem = 0;
                    for (var i = 0; i < list_nhan_vien.length; i++) {
                        var chi_tiet = list_nhan_vien[i].data;
                        if (chi_tiet.AUTO_SELECT == true) {
                            dem += 1;
                            so_tien_hach_toan += chi_tiet.SO_TRA;
                            var ngan_hang_id = 0;
                            var nhan_vien_id = 0;
                            var don_vi_id = 0;
                            if (chi_tiet.NGAN_HANG_ID) {
                                ngan_hang_id = chi_tiet.NGAN_HANG_ID.data.id;
                            }
                            if (chi_tiet.DON_VI_ID) {
                                don_vi_id = chi_tiet.DON_VI_ID.data.id;
                            }
                            if (chi_tiet.MA_NHAN_VIEN_ID) {
                                nhan_vien_id = chi_tiet.MA_NHAN_VIEN_ID.data.id;
                            }
                            arr_list_thong_tin_tra_luong_nhan_vien.push([0, 0, {
                                'MA_NHAN_VIEN': nhan_vien_id,
                                'DON_VI': don_vi_id,
                                'SO_TAI_KHOAN': ngan_hang_id,
                                'TEN_NHAN_VIEN': chi_tiet.TEN_NHAN_VIEN,
                                'TEN_NGAN_HANG': chi_tiet.TEN_NGAN_HANG,
                                'SO_CON_PHAI_TRA': chi_tiet.SO_CON_PHAI_TRA,
                                'SO_TRA': chi_tiet.SO_TRA,
                            }])
                        }
                    }
                    // Kiểm trả điều kiện đã tích chọn nhân viên nào chưa
                    if (dem == 0) {
                        error = 'Bạn chưa chọn nhân viên để trả lương';
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                        return def;
                    } else {
                        if (record.PHUONG_THUC_THANH_TOAN == 'UY_NHIEM_CHI') {
                            param = {
                                'default_LOAI_CHUNG_TU': 1523,
                                'default_TYPE_NH_Q': 'NGAN_HANG',
                                'default_LOAI_PHIEU': 'PHIEU_CHI',
                                'default_arr_list_thong_tin_tra_luong_nhan_vien': arr_list_thong_tin_tra_luong_nhan_vien,
                                'default_so_tien_hach_toan': so_tien_hach_toan,
                                'default_ngay_tra_luong': ngay_tra_luong,
                            };
                            ref_views = ['account_ex.view_nganhang_phieuchi_form', 'form'];
                            title = "Ủy nhiệm chi trả lương nhân viên";
                        } else if (record.PHUONG_THUC_THANH_TOAN == 'TIEN_MAT') {
                            param = {
                                'default_LOAI_CHUNG_TU': 1026,
                                'default_TYPE_NH_Q': 'QUY',
                                'default_LOAI_PHIEU': 'PHIEU_CHI',
                                'default_arr_list_thong_tin_tra_luong_nhan_vien': arr_list_thong_tin_tra_luong_nhan_vien,
                                'default_so_tien_hach_toan': so_tien_hach_toan,
                                'default_ngay_tra_luong': ngay_tra_luong,
                            };
                            ref_views = ['account_ex.view_account_ex_phieu_chi_chi_form', 'form'];
                            title = "Phiếu chi trả lương nhân viên";
                        }
                        return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                            model: this.model,
                            readonly: false,
                            res_model: 'account.ex.phieu.thu.chi',
                            shouldSaveLocally: false,
                            disable_multiple_selection: true,
                            context: param,
                            title: title,
                            ref_views: [ref_views],
                        })).open();
                        break;
                    }
                    default:
                        this._super.apply(this, arguments);
            }

        },
        _onOpenLink: function (event) {
            event.stopPropagation();
            var self = this;
            var colName = event.data.colName;
            var record = this.model.get(event.data.recordId);
            if (colName == 'LICH_SU_TRA_LUONG') {
                return new dialogs.FormViewDialog(self, {
                    model: this.model,
                    res_model: 'tien.luong.lich.su.tra.luong.form',
                    // params: context,
                    parent_form: self,
                    recordID: record.id,
                    res_id: record.id,
                    title: "Lịch sử trả lương",
                    ref_views: [
                        ['tien_luong.view_tien_luong_lich_su_tra_luong_tham_so_form', 'form']
                    ],
                    size: 'large',
                    readonly: false,
                    disable_multiple_selection: true,
                    shouldSaveLocally: true,
                }).open();
            }
        },
    });

    var TienLuongTraLuongView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TienLuongTraLuongController,
        }),
    });

    view_registry.add('tien_luong_tra_luong_form_tham_so_view', TienLuongTraLuongView);

    return TienLuongTraLuongView;
});