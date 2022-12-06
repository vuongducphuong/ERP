odoo.define('tien_luong.tien_luong_tra_luong_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var TienLuongTraLuongController = FormController.extend({

        _onCreate: function () {
            var self = this;
            new dialogs.FormViewDialog(this, {
                res_model: 'tien.luong.tra.luong.form.tham.so',
                readonly: false,
                title: 'Trả lương',
                shouldSaveLocally: true,
                disable_multiple_selection: true,
                ref_views: [
                    ['tien_luong.view_tien_luong_tra_luong_form_tham_so_tham_so_form', 'form']
                ],
                size: 'huge',
                on_before_saved: function (controller) {
                    var def = $.Deferred();
                    var error = [];
                    var dem = 0;
                    var chi_tiet = controller.getFieldValue('TIEN_LUONG_TRA_LUONG_FORM_THAM_SO_CHI_TIET_IDS');
                    for (var i = 0; i < chi_tiet.length; i++) {
                        if (chi_tiet[i].AUTO_SELECT) {
                            dem = dem + 1;
                        }
                    }
                    if (dem == 0) {
                        error = 'Bạn chưa chọn nhân viên để trả lương.';
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                    } else {
                        def.resolve(true);
                    }
                    return def;
                },
                on_after_saved: function (record, changed) {
                    if (changed) {
                        var list_nhan_vien = record.data.TIEN_LUONG_TRA_LUONG_FORM_THAM_SO_CHI_TIET_IDS.data;
                        var ngay_tra_luong = record.data.NGAY_TRA_LUONG;
                        var arr_list_thong_tin_tra_luong_nhan_vien = [];
                        var so_tien_hach_toan = 0;
                        var phuong_thuc_thanh_toan = record.data.PHUONG_THUC_THANH_TOAN;
                        var context = {};

                        var dem = 0;
                        for (var i in list_nhan_vien) {
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
                        if (phuong_thuc_thanh_toan == 'UY_NHIEM_CHI') {
                            context = {
                                'default_LOAI_CHUNG_TU': 1523,
                                'default_TYPE_NH_Q': 'NGAN_HANG',
                                'default_LOAI_PHIEU': 'PHIEU_CHI',
                                'default_arr_list_thong_tin_tra_luong_nhan_vien': arr_list_thong_tin_tra_luong_nhan_vien,
                                'default_so_tien_hach_toan': so_tien_hach_toan,
                                'default_ngay_tra_luong': ngay_tra_luong,
                            };
                        } else if (phuong_thuc_thanh_toan == 'TIEN_MAT') {
                            context = {
                                'default_LOAI_CHUNG_TU': 1026,
                                'default_TYPE_NH_Q': 'QUY',
                                'default_LOAI_PHIEU': 'PHIEU_CHI',
                                'default_arr_list_thong_tin_tra_luong_nhan_vien': arr_list_thong_tin_tra_luong_nhan_vien,
                                'default_so_tien_hach_toan': so_tien_hach_toan,
                                'default_ngay_tra_luong': ngay_tra_luong,
                            };
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
        },
    });

    var TienLuongTraLuongView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TienLuongTraLuongController,
        }),
    });

    view_registry.add('tien_luong_tra_luong_form_view', TienLuongTraLuongView);

    return TienLuongTraLuongView;
});

odoo.define('tien_luong.tien_luong_tra_luong_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var TienLuongTraLuongController = ListController.extend({
        _onCreate: function () {
            var self = this;
            new dialogs.FormViewDialog(this, {
                res_model: 'tien.luong.tra.luong.form.tham.so',
                readonly: false,
                title: 'Trả lương',
                shouldSaveLocally: true,
                disable_multiple_selection: true,
                ref_views: [
                    ['tien_luong.view_tien_luong_tra_luong_form_tham_so_tham_so_form', 'form']
                ],
                size: 'huge',
                on_before_saved: function (controller) {
                    var def = $.Deferred();
                    var error = [];
                    var dem = 0;
                    var chi_tiet = controller.getFieldValue('TIEN_LUONG_TRA_LUONG_FORM_THAM_SO_CHI_TIET_IDS');
                    for (var i = 0; i < chi_tiet.length; i++) {
                        if (chi_tiet[i].AUTO_SELECT) {
                            dem = dem + 1;
                        }
                    }
                    if (dem == 0) {
                        error = 'Bạn chưa chọn nhân viên để trả lương.';
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                    } else {
                        def.resolve(true);
                    }

                    return def;
                },
                on_after_saved: function (record, changed) {
                    if (changed) {

                        var list_nhan_vien = record.data.TIEN_LUONG_TRA_LUONG_FORM_THAM_SO_CHI_TIET_IDS.data;
                        var ngay_tra_luong = record.data.NGAY_TRA_LUONG;
                        var arr_list_thong_tin_tra_luong_nhan_vien = [];
                        var so_tien_hach_toan = 0;
                        var phuong_thuc_thanh_toan = record.data.PHUONG_THUC_THANH_TOAN;
                        var context = {};

                        var dem = 0;
                        for (var i in list_nhan_vien) {
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
                        if (phuong_thuc_thanh_toan == 'UY_NHIEM_CHI') {
                            context = {
                                'default_LOAI_CHUNG_TU': 1523,
                                'default_TYPE_NH_Q': 'NGAN_HANG',
                                'default_LOAI_PHIEU': 'PHIEU_CHI',
                                'default_arr_list_thong_tin_tra_luong_nhan_vien': arr_list_thong_tin_tra_luong_nhan_vien,
                                'default_so_tien_hach_toan': so_tien_hach_toan,
                                'default_ngay_tra_luong': ngay_tra_luong,
                            };
                        } else if (phuong_thuc_thanh_toan == 'TIEN_MAT') {
                            context = {
                                'default_LOAI_CHUNG_TU': 1026,
                                'default_TYPE_NH_Q': 'QUY',
                                'default_LOAI_PHIEU': 'PHIEU_CHI',
                                'default_arr_list_thong_tin_tra_luong_nhan_vien': arr_list_thong_tin_tra_luong_nhan_vien,
                                'default_so_tien_hach_toan': so_tien_hach_toan,
                                'default_ngay_tra_luong': ngay_tra_luong,
                            };
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
        },
    });

    var TienLuongTraLuongView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TienLuongTraLuongController,
        }),
    });

    view_registry.add('tien_luong_tra_luong_list_view', TienLuongTraLuongView);

    return TienLuongTraLuongView;
});