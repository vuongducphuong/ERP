odoo.define('tien_luong.tien_luong_hach_toan_chi_phi_luong_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var TienLuongHachToanChiPhiLuongController = FormController.extend({
        _onCreate: function () {
            var self = this;
            
            new dialogs.FormViewDialog(this, {
                res_model: 'tien.luong.hach.toan.chi.phi.luong.form.tham.so',
                readonly: false,
                title: 'Chọn bảng lương',
                shouldSaveLocally: true,
                disable_multiple_selection: true,
                size:'medium',
                ref_views: [['tien_luong.view_tien_luong_hach_toan_chi_phi_luong_form_tham_so_tham_so_form', 'form']],
                
                on_after_saved: function (record, changed) {
                    if (changed) {
                        var ten_bang_luong = record.data.BANG_LUONG.data.display_name;
                        var context = {
                            'default_bang_luong': ten_bang_luong,
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
        },
    });
    
    var TienLuongHachToanChiPhiLuongView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TienLuongHachToanChiPhiLuongController,
        }),
    });
    
    view_registry.add('tien_luong_hach_toan_chi_phi_luong_form_view', TienLuongHachToanChiPhiLuongView);
    
    return TienLuongHachToanChiPhiLuongView;
});

odoo.define('tien_luong.tien_luong_hach_toan_chi_phi_luong_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var TienLuongHachToanChiPhiLuongController = ListController.extend({
        _onCreate: function () {
            var self = this;
            new dialogs.FormViewDialog(this, {
                res_model: 'tien.luong.hach.toan.chi.phi.luong.form.tham.so',
                readonly: false,
                title: 'Chọn bảng lương',
                shouldSaveLocally: true,
                disable_multiple_selection: true,
                size:'medium',
                ref_views: [['tien_luong.view_tien_luong_hach_toan_chi_phi_luong_form_tham_so_tham_so_form', 'form']],
                on_after_saved: function (record, changed) {
                    if (changed) {
                        var ten_bang_luong = record.data.BANG_LUONG.data.display_name;
                        var id_bang_luong = record.data.BANG_LUONG.data.id;
                        var context = {
                            'default_bang_luong': ten_bang_luong,
                            'default_id_bang_luong': id_bang_luong,
                        }
                        self.createRecord(context);
                    }
                },
            }).open();
        },
    });
    
    var TienLuongHachToanChiPhiLuongView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TienLuongHachToanChiPhiLuongController,
        }),
    });
    
    view_registry.add('tien_luong_hach_toan_chi_phi_luong_list_view', TienLuongHachToanChiPhiLuongView);
    
    return TienLuongHachToanChiPhiLuongView;
});