odoo.define('purchase_ex.chung_tu_mua_dich_vu_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var ChungTuMuaDichVuController = FormController.extend({

        onViewLoaded: function (e, def) {
            this._changeChiTietSelection();
            if (def) {
                def.resolve();
            }
        },

        onFieldChanged: function (field) {
            var self =this;
            switch (field) {
                case 'LOAI_HOA_DON':
                    this._changeChiTietSelection();
                    break;
                
                case 'DOI_TUONG_ID':
                    var doi_tuong = this.getFieldValue('DOI_TUONG_ID')
                    var doi_tuong_id = doi_tuong ? doi_tuong.id : false;
                    self.getFieldWidget('TK_NHAN_ID').changeDomain([['DOI_TUONG_ID', '=', doi_tuong_id]]);
                    break;
                default:
                    break;
            }



        },

        _changeChiTietSelection: function() {
            var LOAI_HOA_DON = this.getFieldValue('LOAI_HOA_DON');
            if (LOAI_HOA_DON == '1') {
                // Nhận kèm hóa đơn
                this.changeSelectionSource('CHI_TIET_DICH_VU', ['HACH_TOAN', 'THUE', 'THONG_KE']);
            } else {
                this.changeSelectionSource('CHI_TIET_DICH_VU', ['HACH_TOAN', 'THONG_KE']);
            }
        },

        _onButtonClicked: function (event) {
            var self = this;
            event.stopPropagation();
            switch (event.data.attrs.id) {

                case "btn_phan_bo_chiet_khau_mua_dich_vu":
                    return new dialogs.FormParamsDialog(this, _.extend({}, this.nodeOptions, {
                        res_model: 'purchase.ex.phan.bo.chiet.khau.theo.hoa.don',
                        title: 'Phân bổ chiết khấu theo hóa đơn',
                        ref_views: [['purchase_ex.view_purchase_ex_phan_bo_chiet_khau_theo_hoa_don_form', 'form']],
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_selected: function (records) {
                            self.changeFieldValue('PHAN_BO_CHIET_KHAU_JSON_MDV', records)
                        },
                    })).open();

                default:
                    this._super.apply(this, arguments);
            }

        }
    });

    var ChungTuMuaDichVuView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: ChungTuMuaDichVuController,
        }),
    });

    view_registry.add('chung_tu_mua_dich_vu_view', ChungTuMuaDichVuView);

    return ChungTuMuaDichVuView;
});
