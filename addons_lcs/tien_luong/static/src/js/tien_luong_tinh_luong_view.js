odoo.define('tien_luong.tien_luong_tinh_luong_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');


    var TienLuongTinhLuongController = FormController.extend({
        _onCreate: function () {
            var self = this;
            new dialogs.FormViewDialog(this, {
                res_model: 'tien.luong.bang.luong.form.tham.so',
                title: 'Tạo bảng lương',
                readonly: false,
                ref_views: [
                    ['tien_luong.view_tien_luong_bang_luong_form_tham_so_tham_so_form', 'form']
                ],
                size: 'large',
                shouldSaveLocally: true,
                disable_multiple_selection: true,

                on_before_saved: function (controller) {
                    var def = $.Deferred();
                    var error = [];
                    var dem = 0;
                    var chi_tiet = controller.getFieldValue('DON_VI_IDS');
                    for (var i = 0; i < chi_tiet.length; i++) {
                        if (chi_tiet[i].AUTO_SELECT) {
                            dem = dem + 1;
                        }
                    }
                    if (dem == 0) {
                        error = 'Bạn chưa chọn đơn vị.Xin vui lòng chọn lại.';
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                    } else {
                        var dam_bao_check_du_dieu_kien = true;
                        var hinh_thuc_tao_bang_luong = controller.getFieldValue('HINH_THUC_TAO_BANG_LUONG');
                        var bang_luong = controller.getFieldValue('BANG_LUONG');
                        if (hinh_thuc_tao_bang_luong == 'DUA_TREN_BANG_LUONG_KHAC') {
                            if (!bang_luong) {
                                dam_bao_check_du_dieu_kien = false;
                                error = 'Bạn phải chọn ít nhất một Bảng lương dựa trên.';
                                self.notifyInvalidFields(error);
                                def.resolve(false);
                            } else {
                                dam_bao_check_du_dieu_kien = true;
                            }
                        }
                        if (dam_bao_check_du_dieu_kien == true) {
                            var thang = controller.getFieldValue('THANG');
                            var nam = controller.getFieldValue('NAM');
                            controller.rpc_action({
                                model: 'tien.luong.bang.luong.form.tham.so',
                                method: 'kiem_tra_ton_tai_bang_luong',
                                args: {
                                    'thang': thang,
                                    'nam': nam,
                                },
                                callback: function (result) {
                                    if (result != 0) {
                                        var string_Thang_Nam = 'Bảng lương ' + String(thang) + ' năm ' + String(nam) + ' đã tồn tại.';
                                        error = string_Thang_Nam;
                                        self.notifyInvalidFields(error);
                                        def.resolve(false);

                                    } else {
                                        def.resolve(true);
                                    }
                                }
                            });
                        }

                    }
                    return def;
                },

                on_after_saved: function (record, changed) {
                    if (changed) {
                        var ten_bang_luong = record.data.TEN_BANG_LUONG;
                        var ten_loai_bang_luong = record.data.LOAI_BANG_LUONG;
                        var thang = record.data.THANG;
                        var nam = record.data.NAM;
                        var HINH_THUC_TAO_BANG_LUONG = record.data.HINH_THUC_TAO_BANG_LUONG;
                        var BANG_LUONG = record.data.BANG_LUONG;
                        var TU_DONG_THEM_VAO_CAC_NHAN_VIEN_MOI = record.data.TU_DONG_THEM_VAO_CAC_NHAN_VIEN_MOI;
                        var LAY_CA_NHAN_VIEN_NGUNG_THEO_DOI = record.data.LAY_CA_NHAN_VIEN_NGUNG_THEO_DOI;
                        if (record.data.DON_VI_IDS.data.length > 0) {
                            var arr_list_don_vi = [];
                            for (var i in record.data.DON_VI_IDS.data) {
                                var chi_tiet = record.data.DON_VI_IDS.data[i].data;
                                if (chi_tiet.AUTO_SELECT == true) {
                                    arr_list_don_vi.push(
                                        chi_tiet.DON_VI_ID,
                                    )
                                }
                            }
                        }
                        if (BANG_LUONG) {
                            var BANG_LUONG_id = record.data.BANG_LUONG.data.id;
                        }
                        var context = {
                            'default_TEN_BANG_LUONG': ten_bang_luong,
                            'default_TEN_LOAI_BANG_LUONG': ten_loai_bang_luong,
                            'default_THANG': thang,
                            'default_NAM': nam,
                            'default_arr_list_don_vi': arr_list_don_vi,
                            'default_hinh_thuc_tao_bang_luong': HINH_THUC_TAO_BANG_LUONG,
                            'default_bang_luong_id': BANG_LUONG_id,
                            'default_TU_DONG_THEM_VAO_CAC_NHAN_VIEN_MOI': TU_DONG_THEM_VAO_CAC_NHAN_VIEN_MOI,
                            'default_LAY_CA_NHAN_VIEN_NGUNG_THEO_DOI': LAY_CA_NHAN_VIEN_NGUNG_THEO_DOI,
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
        },
    });

    var TienLuongTinhLuongView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TienLuongTinhLuongController,
        }),
    });

    view_registry.add('tien_luong_tinh_luong_form_view', TienLuongTinhLuongView);

    return TienLuongTinhLuongView;
});

odoo.define('tien_luong.tien_luong_tinh_luong_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');


    var TienLuongTinhLuongController = ListController.extend({
        _onCreate: function () {
            var self = this;
            new dialogs.FormViewDialog(this, {
                res_model: 'tien.luong.bang.luong.form.tham.so',
                title: 'Tạo bảng lương',
                readonly: false,
                ref_views: [
                    ['tien_luong.view_tien_luong_bang_luong_form_tham_so_tham_so_form', 'form']
                ],
                size: 'large',
                shouldSaveLocally: true,
                disable_multiple_selection: true,

                on_before_saved: function (controller) {
                    var def = $.Deferred();
                    var error = [];
                    var dem = 0;
                    var chi_tiet = controller.getFieldValue('DON_VI_IDS');
                    for (var i = 0; i < chi_tiet.length; i++) {
                        if (chi_tiet[i].AUTO_SELECT) {
                            dem = dem + 1;
                        }
                    }
                    if (dem == 0) {
                        error = 'Bạn chưa chọn đơn vị.Xin vui lòng chọn lại.';
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                    } else {
                        var dam_bao_check_du_dieu_kien = true;
                        var hinh_thuc_tao_bang_luong = controller.getFieldValue('HINH_THUC_TAO_BANG_LUONG');
                        var bang_luong = controller.getFieldValue('BANG_LUONG');
                        if (hinh_thuc_tao_bang_luong == 'DUA_TREN_BANG_LUONG_KHAC') {
                            if (!bang_luong) {
                                dam_bao_check_du_dieu_kien = false;
                                error = 'Bạn phải chọn ít nhất một Bảng lương dựa trên.';
                                self.notifyInvalidFields(error);
                                def.resolve(false);
                            } else {
                                dam_bao_check_du_dieu_kien = true;
                            }
                        }
                        if (dam_bao_check_du_dieu_kien == true) {
                            var thang = controller.getFieldValue('THANG');
                            var nam = controller.getFieldValue('NAM');
                            controller.rpc_action({
                                model: 'tien.luong.bang.luong.form.tham.so',
                                method: 'kiem_tra_ton_tai_bang_luong',
                                args: {
                                    'thang': thang,
                                    'nam': nam,
                                },
                                callback: function (result) {
                                    if (result != 0) {
                                        var string_Thang_Nam = 'Bảng lương ' + String(thang) + ' năm ' + String(nam) + ' đã tồn tại.';
                                        error = string_Thang_Nam;
                                        self.notifyInvalidFields(error);
                                        def.resolve(false);

                                    } else {
                                        def.resolve(true);
                                    }
                                }
                            });
                        }

                    }
                    return def;
                },

                on_after_saved: function (record, changed) {
                    if (changed) {
                        var ten_bang_luong = record.data.TEN_BANG_LUONG;
                        var ten_loai_bang_luong = record.data.LOAI_BANG_LUONG;
                        var thang = record.data.THANG;
                        var nam = record.data.NAM;
                        var HINH_THUC_TAO_BANG_LUONG = record.data.HINH_THUC_TAO_BANG_LUONG;
                        var BANG_LUONG = record.data.BANG_LUONG;
                        var TU_DONG_THEM_VAO_CAC_NHAN_VIEN_MOI = record.data.TU_DONG_THEM_VAO_CAC_NHAN_VIEN_MOI;
                        var LAY_CA_NHAN_VIEN_NGUNG_THEO_DOI = record.data.LAY_CA_NHAN_VIEN_NGUNG_THEO_DOI;
                        if (record.data.DON_VI_IDS.data.length > 0) {
                            var arr_list_don_vi = [];
                            for (var i in record.data.DON_VI_IDS.data) {
                                var chi_tiet = record.data.DON_VI_IDS.data[i].data;
                                if (chi_tiet.AUTO_SELECT == true) {
                                    arr_list_don_vi.push(
                                        chi_tiet.DON_VI_ID,
                                    )
                                }
                            }
                        }
                        if (BANG_LUONG) {
                            var BANG_LUONG_id = record.data.BANG_LUONG.data.id;
                        }
                        var context = {
                            'default_TEN_BANG_LUONG': ten_bang_luong,
                            'default_TEN_LOAI_BANG_LUONG': ten_loai_bang_luong,
                            'default_THANG': thang,
                            'default_NAM': nam,
                            'default_arr_list_don_vi': arr_list_don_vi,
                            'default_hinh_thuc_tao_bang_luong': HINH_THUC_TAO_BANG_LUONG,
                            'default_bang_luong_id': BANG_LUONG_id,
                            'default_TU_DONG_THEM_VAO_CAC_NHAN_VIEN_MOI': TU_DONG_THEM_VAO_CAC_NHAN_VIEN_MOI,
                            'default_LAY_CA_NHAN_VIEN_NGUNG_THEO_DOI': LAY_CA_NHAN_VIEN_NGUNG_THEO_DOI,
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
        },
    });

    var TienLuongTinhLuongView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TienLuongTinhLuongController,
        }),
    });

    view_registry.add('tien_luong_tinh_luong_list_view', TienLuongTinhLuongView);

    return TienLuongTinhLuongView;
});