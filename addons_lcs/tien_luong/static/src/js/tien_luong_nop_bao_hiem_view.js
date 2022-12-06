odoo.define('tien_luong.tien_luong_nop_tien_bao_hiem_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var TienLuongNopBaoHiemController = FormController.extend({

        _onCreate: function () {
            var self = this;
            new dialogs.FormViewDialog(this, {
                res_model: 'tien.luong.nop.bao.hiem.form.tham.so',
                readonly: false,
                title: 'Nộp bảo hiểm',
                shouldSaveLocally: true,
                disable_multiple_selection: true,
                ref_views: [
                    ['tien_luong.view_tien_luong_nop_bao_hiem_form_tham_so_tham_so_form', 'form']
                ],
                size: 'huge',
                on_before_saved: function (controller) {
                    var def = $.Deferred();
                    var error = [];
                    var dem = 0;
                    var chi_tiet = controller.getFieldValue('TIEN_LUONG_NOP_BAO_HIEM_FORM_THAM_SO_CHI_TIET_IDS');
                    for (var i = 0; i < chi_tiet.length; i++) {
                        if (chi_tiet[i].AUTO_SELECT) {
                            dem = dem + 1;
                        }
                    }
                    if (dem == 0) {
                        error = 'Bạn chưa chọn khoản bảo hiểm nào.';
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                    } else {
                        def.resolve(true);
                    }
                    return def;
                },
                on_after_saved: function (record, changed) {
                    if (changed) {
                        var list_bao_hiem = record.data.TIEN_LUONG_NOP_BAO_HIEM_FORM_THAM_SO_CHI_TIET_IDS.data;
                        var ngay_nop_bao_hiem = record.data.NGAY_NOP_BAO_HIEM;
                        var arr_list_thong_tin_nop_bao_hiem = [];
                        var phuong_thuc_thanh_toan = record.data.PHUONG_THUC_THANH_TOAN;
                        var context = {};
                        for (var i in list_bao_hiem) {
                            var chi_tiet = list_bao_hiem[i].data;
                            if (chi_tiet.AUTO_SELECT == true) {
                                arr_list_thong_tin_nop_bao_hiem.push([0, 0, {
                                    'DIEN_GIAI_DETAIL': chi_tiet.KHOAN_PHAI_NOP,
                                    'TK_NO_ID': chi_tiet.SO_TAI_KHOAN_ID.data.id,
                                    'SO_TIEN': chi_tiet.SO_NOP_LAN_NAY,
                                }])
                            }
                        }
                        if (phuong_thuc_thanh_toan == 'UY_NHIEM_CHI') {
                            context = {
                                'default_LOAI_CHUNG_TU': 1522,
                                'default_TYPE_NH_Q': 'NGAN_HANG',
                                'default_LOAI_PHIEU': 'PHIEU_CHI',
                                'default_arr_list_thong_tin_nop_bao_hiem': arr_list_thong_tin_nop_bao_hiem,
                                'default_ngay_nop_bao_hiem': ngay_nop_bao_hiem,
                            };
                        } else if (phuong_thuc_thanh_toan == 'TIEN_MAT') {
                            context = {
                                'default_LOAI_CHUNG_TU': 1025,
                                'default_TYPE_NH_Q': 'QUY',
                                'default_LOAI_PHIEU': 'PHIEU_CHI',
                                'default_arr_list_thong_tin_nop_bao_hiem': arr_list_thong_tin_nop_bao_hiem,
                                'default_ngay_nop_bao_hiem': ngay_nop_bao_hiem,
                            };
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
        },
    });

    var TienLuongNopBaoHiemView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TienLuongNopBaoHiemController,
        }),
    });

    view_registry.add('tien_luong_nop_tien_bao_hiem_form_view', TienLuongNopBaoHiemView);

    return TienLuongNopBaoHiemView;
});

odoo.define('tien_luong.tien_luong_nop_tien_bao_hiem_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var TienLuongNopBaoHiemController = ListController.extend({
        _onCreate: function () {
            var self = this;
            new dialogs.FormViewDialog(this, {
                res_model: 'tien.luong.nop.bao.hiem.form.tham.so',
                readonly: false,
                title: 'Nộp bảo hiểm',
                shouldSaveLocally: true,
                disable_multiple_selection: true,
                ref_views: [
                    ['tien_luong.view_tien_luong_nop_bao_hiem_form_tham_so_tham_so_form', 'form']
                ],
                size: 'huge',
                on_before_saved: function (controller) {
                    var def = $.Deferred();
                    var error = [];
                    var dem = 0;
                    var chi_tiet = controller.getFieldValue('TIEN_LUONG_NOP_BAO_HIEM_FORM_THAM_SO_CHI_TIET_IDS');
                    for (var i = 0; i < chi_tiet.length; i++) {
                        if (chi_tiet[i].AUTO_SELECT) {
                            dem = dem + 1;
                        }
                    }
                    if (dem == 0) {
                        error = 'Bạn chưa chọn khoản bảo hiểm nào.';
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                    } else {
                        def.resolve(true);
                    }
                    return def;
                },
                on_after_saved: function (record, changed) {
                    if (changed) {
                        var list_bao_hiem = record.data.TIEN_LUONG_NOP_BAO_HIEM_FORM_THAM_SO_CHI_TIET_IDS.data;
                        var ngay_nop_bao_hiem = record.data.NGAY_NOP_BAO_HIEM;
                        var arr_list_thong_tin_nop_bao_hiem = [];
                        var phuong_thuc_thanh_toan = record.data.PHUONG_THUC_THANH_TOAN;
                        var context = {};
                        for (var i in list_bao_hiem) {
                            var chi_tiet = list_bao_hiem[i].data;
                            if (chi_tiet.AUTO_SELECT == true) {
                                arr_list_thong_tin_nop_bao_hiem.push([0, 0, {
                                    'DIEN_GIAI_DETAIL': chi_tiet.KHOAN_PHAI_NOP,
                                    'TK_NO_ID': chi_tiet.SO_TAI_KHOAN_ID.data.id,
                                    'SO_TIEN': chi_tiet.SO_NOP_LAN_NAY,
                                }])
                            }
                        }
                        if (phuong_thuc_thanh_toan == 'UY_NHIEM_CHI') {
                            context = {
                                'default_LOAI_CHUNG_TU': 1522,
                                'default_TYPE_NH_Q': 'NGAN_HANG',
                                'default_LOAI_PHIEU': 'PHIEU_CHI',
                                'default_arr_list_thong_tin_nop_bao_hiem': arr_list_thong_tin_nop_bao_hiem,
                                'default_ngay_nop_bao_hiem': ngay_nop_bao_hiem,
                            };
                        } else if (phuong_thuc_thanh_toan == 'TIEN_MAT') {
                            context = {
                                'default_LOAI_CHUNG_TU': 1025,
                                'default_TYPE_NH_Q': 'QUY',
                                'default_LOAI_PHIEU': 'PHIEU_CHI',
                                'default_arr_list_thong_tin_nop_bao_hiem': arr_list_thong_tin_nop_bao_hiem,
                                'default_ngay_nop_bao_hiem': ngay_nop_bao_hiem,
                            };
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
        },
    });

    var TienLuongNopBaoHiemView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TienLuongNopBaoHiemController,
        }),
    });

    view_registry.add('tien_luong_nop_tien_bao_hiem_list_view', TienLuongNopBaoHiemView);

    return TienLuongNopBaoHiemView;
});