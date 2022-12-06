odoo.define('tien_luong.tien_luong_tao_bang_luong_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var TienLuongTaoBangLuongController = FormController.extend({
        onViewLoaded: function(e, defer) {
            this._changeChiTietSelection();
            if (defer) {
                defer.resolve();
            }
        },

        onFieldChanged: function (field) {
            if (field == 'LOAI_BANG_LUONG') {
                this._changeChiTietSelection();
            }
        },

        _changeChiTietSelection: function() {
            var LOAI_BANG_LUONG = this.getFieldValue('LOAI_BANG_LUONG')
            if (LOAI_BANG_LUONG == 'LUONG_CO_DINH') {
                this.getFieldWidget('BANG_LUONG').changeDomain([
                    ['TEN_LOAI_BANG_LUONG', '=', 'LUONG_CO_DINH']
                ]);
            } else if (LOAI_BANG_LUONG == 'LUONG_THOI_GIAN_THEO_BUOI') {
                this.getFieldWidget('BANG_LUONG').changeDomain([
                    ['TEN_LOAI_BANG_LUONG', '=', 'LUONG_THOI_GIAN_THEO_BUOI']
                ]);
            } else if (LOAI_BANG_LUONG == 'LUONG_THOI_GIAN_THEO_GIO') {
                this.getFieldWidget('BANG_LUONG').changeDomain([
                    ['TEN_LOAI_BANG_LUONG', '=', 'LUONG_THOI_GIAN_THEO_GIO']
                ]);
            } else if (LOAI_BANG_LUONG == 'LUONG_TAM_UNG') {
                this.getFieldWidget('BANG_LUONG').changeDomain([
                    ['TEN_LOAI_BANG_LUONG', '=', 'LUONG_TAM_UNG']
                ]);
            }
        },
    });

    var TienLuongTaoBangLuongView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TienLuongTaoBangLuongController,
        }),
    });

    view_registry.add('tien_luong_tao_bang_luong_form_view', TienLuongTaoBangLuongView);

    return TienLuongTaoBangLuongView;
});