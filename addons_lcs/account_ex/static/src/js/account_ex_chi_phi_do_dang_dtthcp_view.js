odoo.define('account_ex.account_ex_chi_phi_do_dang_dtthcp_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var Dialog = require('web.Dialog');

    var ChiPhiDoDangDTTHCPController = FormController.extend({
        onViewLoaded: function (e, defer) {
            var self = this;
            var def = defer;

            this.rpc_action({
                model: 'account.ex.chi.phi.do.dang.master',
                method: 'lay_du_lieu_dtthcp',
                // args: {},
                callback: function (result) {
                    if (result) {
                        self.updateUI(result).then(function() {
                            var nhap_chi_tiet = self.getFieldValue('NHAP_CHI_TIET_LOAI_CPDD_DTTHCP');
                            var fieldWidget = self.getFieldWidget('ACCOUNT_EX_CHI_PHI_DO_DANG_IDS');
                            if(nhap_chi_tiet == true){
                                fieldWidget.do_visible_columns(['NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','KHAU_HAO','CHI_PHI_MUA_NGOAI','CHI_PHI_KHAC','CHI_PHI_NVL_GIAN_TIEP','CHI_PHI_KHAU_HAO'], true);
                                fieldWidget.do_visible_columns(['CHI_PHI_CHUNG'], false);
                            }
                        	else{
                                fieldWidget.do_visible_columns(['NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','KHAU_HAO','CHI_PHI_MUA_NGOAI','CHI_PHI_KHAC','CHI_PHI_NVL_GIAN_TIEP','CHI_PHI_KHAU_HAO'], false);
                                fieldWidget.do_visible_columns(['CHI_PHI_CHUNG'], true);
                            }
							// fieldWidget.do_visible_columns(['NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','KHAU_HAO','CHI_PHI_MUA_NGOAI','CHI_PHI_KHAC'], false);
                        	if (def) {
								def.resolve();
							}
                        });
                    }
                }
            });
        },
        onFieldChanged: function(field){
            var self = this;
            if("NHAP_CHI_TIET_LOAI_CPDD_DTTHCP" == field){
            		
					Dialog.show_message('', 'Nếu tích chọn Nhập chi tiết theo các yếu tố chi phí thì số liệu bạn nhập trên khoản mục Chi phí chung sẽ hiển thị trên yếu tố Chi phí khác. Bạn có muốn tiếp tục thực hiện không?', 'CONFIRM')
					.then(function(result) {
                        var fieldWidget = self.getFieldWidget('ACCOUNT_EX_CHI_PHI_DO_DANG_IDS');
						if(result == true){
                            if(self.getFieldValue('NHAP_CHI_TIET_LOAI_CPDD_DTTHCP') == true){
                                fieldWidget.do_visible_columns(['NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','KHAU_HAO','CHI_PHI_MUA_NGOAI','CHI_PHI_KHAC','CHI_PHI_NVL_GIAN_TIEP','CHI_PHI_KHAU_HAO'], true);
                                fieldWidget.do_visible_columns(['CHI_PHI_CHUNG'], false);
                            }
                            else{
                                fieldWidget.do_visible_columns(['NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','KHAU_HAO','CHI_PHI_MUA_NGOAI','CHI_PHI_KHAC','CHI_PHI_NVL_GIAN_TIEP','CHI_PHI_KHAU_HAO'], false);
                                fieldWidget.do_visible_columns(['CHI_PHI_CHUNG'], true);
                            }
                        }
				});
            }
        },
//         onRowChanged: function(field, columnName, newValue, recordValue, record){
//         	var self = this;
//             if('NVL_GIAN_TIEP' == columnName || 'CHI_PHI_NHAN_CONG_GIAN_TIEP' == columnName || 'KHAU_HAO' == columnName || 'CHI_PHI_MUA_NGOAI' == columnName){
//                 var tong_chi_phi = 0;
//                 tong_chi_phi = ((recordValue.NVL_GIAN_TIEP === undefined) ? 0 : recordValue.NVL_GIAN_TIEP)
//                 + ((recordValue.CHI_PHI_NHAN_CONG_GIAN_TIEP === undefined) ? 0 : recordValue.CHI_PHI_NHAN_CONG_GIAN_TIEP)
//                 + ((recordValue.KHAU_HAO === undefined) ? 0 : recordValue.KHAU_HAO)
//                 + ((recordValue.CHI_PHI_MUA_NGOAI === undefined) ? 0 : recordValue.CHI_PHI_MUA_NGOAI);
//                 self.updateUI({'ACCOUNT_EX_CHI_PHI_DO_DANG_IDS': [[1, record.id, {'TONG_CHI_PHI': tong_chi_phi}]]});
//             }
//         }
    });

    var ChiPhiDoDangDTTHCPView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: ChiPhiDoDangDTTHCPController,
        }),
    });

    view_registry.add('account_ex_chi_phi_do_dang_dtthcp_form_view', ChiPhiDoDangDTTHCPView);

    return ChiPhiDoDangDTTHCPView;
});