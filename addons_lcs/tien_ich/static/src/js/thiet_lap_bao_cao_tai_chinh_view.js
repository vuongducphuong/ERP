odoo.define('tien_ich.thiet_lap_bao_cao_tai_chinh_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var ThietLapBaoCaoTaiChinhController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {
                case "btn_lay_gia_tri_mac_dinh":
                    // self.changeFieldValue('STEP', 2);
                    this.rpc_action({
                        model: 'tien.ich.thiet.lap.bao.cao.tai.chinh',
                        method: 'thuc_hien_lay_gia_tri_mac_dinh',
                        // args: {},
                        callback: function(result) {
                            self.updateUI(result);
                        }
                    })
                    break;
                
                

                case "btn_kiem_tra_cong_thuc_trung_lap":
                    return new dialogs.SelectParamsDialog(this, _.extend({}, this.nodeOptions, {
                        res_model: 'tien.ich.kiem.tra.cong.thuc.thiet.lap.trung.lap',
                        title: 'Kiểm tra công thức bị thiết lập trùng lặp',
                        ref_views: [['tien_ich.view_tien_ich_kiem_tra_cong_thuc_thiet_lap_trung_lap_tham_so_form', 'form']],
                        // context: _.extend(event.data.record.context || {}, event.data.record.data || {}),
                        on_selected: function (records) {
                            // self.changeFieldValue('PHAN_BO_CHIET_KHAU_JSON_MDV', records)
                        },
                    })).open();
                    break;
                    
                default: 
                   this._super.apply(this, arguments);
                   break;
            }
            
        },

        _onOpenLink: function (event) {
            event.stopPropagation();
            var self = this;
            var ref_views = [];
            var colName = event.data.colName;
            var data_for_many2one = false;
            switch (colName) {
                case 'CONG_THUC':
                    ref_views = [['tien_ich.view_tien_ich_bao_cao_tai_chinh_chi_tiet_form', 'form']];
                    data_for_many2one = _.map(this.getFieldValue('TIEN_ICH_BAO_CAO_TAI_CHINH_CHI_TIET_IDS'), function(change){ 
                        return {
                            MA_CHI_TIEU: change.MA_CHI_TIEU,
                            TEN_CHI_TIEU: change.TEN_CHI_TIEU,
                            id: change.ID_CHI_TIEU,
                            value: change.MA_CHI_TIEU,
                        } 
                    });
                    break;
                case 'SO_CON_PHAI_NOP_KY_TRUOC_CHUYEN_SANG':
                    ref_views = [['tien_ich.view_tien_ich_tinh_hinh_thnvdvnnpnkt_chi_tiet_form', 'form']];
                    break;
                case 'SO_PHAI_NOP_TRONG_KY':
                    ref_views = [['tien_ich.view_tien_ich_tinh_hinh_thnvdvnnpntk_chi_tiet_form', 'form']];
                    break;
                case 'CUOI_NAM':
                    ref_views = [['tien_ich.view_tien_ich_thuyet_minh_bao_cao_tai_chinh_chi_tiet_form', 'form']];
                    break;
                case 'DAU_NAM':
                    ref_views = [['tien_ich.view_tien_ich_thuyet_minh_bao_cao_tai_chinh_chi_tiet_form', 'form']];
                    break;
                default:
                    break;
            }
            var record = this.model.get(event.data.recordId);
            var ten_bao_cao = this.getFieldValue("TEN_BAO_CAO");
            return new dialogs.FormViewDialog(self, {
                ten_bao_cao: ten_bao_cao,
                ma_chi_tieu: record.data.MA_CHI_TIEU,
                //fields_view: data.fields_view,
                model: this.model,
                //parentID: data.parentID,
                readonly: this.mode == "readonly",
                recordID: record.id,
                res_id: record.res_id,
                res_model: record.model,
                shouldSaveLocally: true,
                disable_multiple_selection: true,
                title: "Xây dựng công thức",
                ref_views: ref_views,
                field: event.data.field,
                colName: colName,
                data_for_many2one: data_for_many2one,
            }).open();
        },

        onViewLoaded(e, defer) {
            // this.cActiveCurrentTab();
            if (defer) {
                defer.resolve();
            }
        },

        onFieldChanged(field) {
            switch (field) {
                case 'THUYET_MINH_BAO_CAO_TAI_CHINH_TAB':
                    // var current_tab = this.getFieldValue('THUYET_MINH_BAO_CAO_TAI_CHINH_TAB');
                    // var fieldWidget = this.getFieldWidget('TIEN_ICH_THUYET_MINH_BAO_CAO_TAI_CHINH_CHI_TIET_IDS');
                    // fieldWidget.do_filter(['PART_IN_TAB', '=', current_tab]);
                    // this.cActiveCurrentTab();
                    break;
                default:
                    break;
            }
        },

        cActiveCurrentTab() {
            var current_tab = this.getFieldValue('THUYET_MINH_BAO_CAO_TAI_CHINH_TAB');
            var fieldWidget = this.getFieldWidget('TIEN_ICH_THUYET_MINH_BAO_CAO_TAI_CHINH_CHI_TIET_IDS');
            fieldWidget.do_filter(['tab', '=', current_tab]);
        },
    });

    var ThietLapBaoCaoTaiChinhRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var ThietLapBaoCaoTaiChinhModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var ThietLapBaoCaoTaiChinhView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: ThietLapBaoCaoTaiChinhModel,
            Renderer: ThietLapBaoCaoTaiChinhRenderer,
            Controller: ThietLapBaoCaoTaiChinhController,
        }),
    });
    
    view_registry.add('thiet_lap_bao_cao_tai_chinh_view', ThietLapBaoCaoTaiChinhView);
    
    return ThietLapBaoCaoTaiChinhView;
});
