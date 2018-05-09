import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkinter import ttk, messagebox, filedialog
from sow_db import SOW_Database



class GUI:
    def __init__(self, master):
        self.master = master

        # configure row & column
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=100)

        # frames
        self.frame0 = tk.Frame(self.master)
        self.frame0.grid(row=0, column=0, sticky='we', padx=10, pady=(20,10))
        self.frame1 = tk.Frame(self.master)
        self.frame1.grid(row=1, column=0, sticky='we', padx=10, pady=10)
        self.frame2 = tk.Frame(self.master)
        self.frame2.grid(row=2, column=0, sticky='nswe')
        self.frame3 = tk.Frame(self.master)
        self.frame3.grid(row=3, column=0, sticky='we')

        # navigation & edit
        self.add_nav_new_edit()

        # populate master window with labels and entries to capture data for row
        self.add_labels_entries()

        # add treeview and populate it
        db = SOW_Database()
        rows = db.sow_records()
        self.treeview_main = ttk.Treeview(self.frame2)
        self.treeview_main.pack(expand=True, fill=tk.BOTH)
        self.treeview_main.bind('<ButtonRelease-1>',
                                lambda event, arg=self.treeview_main: self.treeview_item_click(event, arg))
        self.add_horizontal_scroll_bars(self.frame3, self.treeview_main)
        self.add_vertical_scroll_bars(self.master, 2, 1, self.treeview_main)
        self.populate_treeview(self.treeview_main, db, rows)

        # populate entry box for edit
        self.populate_data_for_edit(self.treeview_main, 1)

    def add_nav_new_edit(self):
        # Add navigation, edit and search on top of window
        frm = self.frame0
        padx_amt = 1
        btn_size = 3

        # Start: nav
        grp_nav = ttk.LabelFrame(frm, text='Navigate/New/Save/Delete')
        grp_nav.pack(side=tk.LEFT)
        # first
        btn_first = ttk.Button(grp_nav, text='|<', width=btn_size)
        btn_first.pack(side=tk.LEFT)
        btn_first.bind('<Button-1>', self.navigate_records)
        # previous
        btn_previous = ttk.Button(grp_nav, text='<', width=btn_size)
        btn_previous.pack(side=tk.LEFT)
        btn_previous.bind('<Button-1>', self.navigate_records)
        # next
        btn_next = ttk.Button(grp_nav, text='>', width=btn_size)
        btn_next.pack(side=tk.LEFT)
        btn_next.bind('<Button-1>', self.navigate_records)
        # last
        btn_last = ttk.Button(grp_nav, text='>|', width=btn_size)
        btn_last.pack(side=tk.LEFT)
        btn_last.bind('<Button-1>', self.navigate_records)
        # new
        btn_new = ttk.Button(grp_nav, text='New', width=btn_size + 2, command=self.add_new_command)
        btn_new.pack(side=tk.LEFT)
        # save
        btn_save = ttk.Button(grp_nav, text='Save', width=btn_size + 2, command=self.save_record_command)
        btn_save.pack(side=tk.LEFT)
        # delete
        btn_delete = ttk.Button(grp_nav, text='Delete', width=btn_size + 3, command=self.delete_command)
        btn_delete.pack(side=tk.LEFT)
        #End: nav

        # Start: group box - search
        grp_box = ttk.LabelFrame(frm, text='Search')
        grp_box.pack(side=tk.LEFT, padx=10)
        # sow name
        lbl_sow_name = ttk.Label(grp_box, text='SOW Name')
        lbl_sow_name.pack(side=tk.LEFT)
        self.ent_sow_name_search = ttk.Entry(grp_box)
        self.ent_sow_name_search.pack(side=tk.LEFT, padx=padx_amt)
        # sow owner wipro
        lbl_sow_owner_wipro = ttk.Label(grp_box, text='SOW Owner (Wipro)')
        lbl_sow_owner_wipro.pack(side=tk.LEFT)
        self.ent_sow_owner_wipro_search = ttk.Entry(grp_box)
        self.ent_sow_owner_wipro_search.pack(side=tk.LEFT, padx=padx_amt)
        # sow owner chc
        lbl_sow_owner_chc = ttk.Label(grp_box, text='SOW Owner (CHC)')
        lbl_sow_owner_chc.pack(side=tk.LEFT)
        self.ent_sow_owner_chc_search = ttk.Entry(grp_box)
        self.ent_sow_owner_chc_search.pack(side=tk.LEFT, padx=padx_amt)
        # search button
        btn_search = ttk.Button(grp_box, text='Search', width=6, command=self.search_command)
        btn_search.pack(side=tk.LEFT, padx=padx_amt)
        # End: group box - search

        # Start: group box - Import data and Visualization
        # grp box
        grp_import_visual = ttk.LabelFrame(frm, text='Import Data/Visualization')
        grp_import_visual.pack(side=tk.LEFT)
        # import button
        btn_import = ttk.Button(grp_import_visual, text='Import Data', command=self.import_data_command)
        btn_import.pack(side=tk.LEFT)
        # visualization button
        btn_visual = ttk.Button(grp_import_visual, text='Visualization', command=self.add_visualization_win)
        btn_visual.pack(side=tk.LEFT)
        # End: group box - Import data and Visualization

    def add_visualization_win(self):
        # Adds visualization window
        vis_win = tk.Toplevel()
        vis_win.title('Visualization')
        vis_win.geometry('800x600')
        vis_win.grab_set()
        vis_win.columnconfigure(0, weight=1)
        vis_win.rowconfigure(0, weight=1)
        vis_win.rowconfigure(1, weight=100)

        # top frame - chart
        top_frame = tk.Frame(vis_win, height=300, bg='yellow')
        top_frame.grid(row=0, column=0)
        # middle frame - treeview
        mid_frame = tk.Frame(vis_win)
        mid_frame.grid(row=1, column=0, sticky='nswe')
        # bottom frame - horizontal scrollbar
        btm_frame = tk.Frame(vis_win)
        btm_frame.grid(row=2, column=0, sticky='we')

        treeview_visual = ttk.Treeview(mid_frame)
        treeview_visual.pack(expand=True, fill=tk.BOTH)
        self.add_vertical_scroll_bars(vis_win, 1, 1, treeview_visual)
        self.add_horizontal_scroll_bars(btm_frame, treeview_visual)
        db = SOW_Database()
        rows = db.sow_records()
        self.populate_treeview(treeview_visual, db, rows)

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8], [5,6,1,3,8,9,3,5])

        canvas = FigureCanvasTkAgg(f, top_frame)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def add_labels_entries(self):
        # populate master window with labels and entries to capture data for row

        frm = self.frame1
        left_align = 'w'
        both_align = 'we'
        pad_y_amt = 2
        pad_x_amt = 5

        # s. no
        lbl_sno_name = ttk.Label(frm, text='S. No')
        lbl_sno_name.grid(row=0, column=0, sticky=left_align, pady=pad_y_amt)
        self.lbl_sno_value = ttk.Label(frm, text='', relief=tk.SUNKEN, anchor=tk.CENTER)
        self.lbl_sno_value.grid(row=0, column=1, sticky=both_align, pady=pad_y_amt, padx=pad_x_amt)
        # bu code
        lbl_bu_code = ttk.Label(frm, text='BU Code')
        lbl_bu_code.grid(row=1, column=0, sticky=left_align, pady=pad_y_amt)
        self.ent_bu_code = ttk.Entry(frm)
        self.ent_bu_code.grid(row=1, column=1, sticky=both_align, pady=pad_y_amt, padx=pad_x_amt)
        # sow id
        lbl_sow_id = ttk.Label(frm, text='SOW ID')
        lbl_sow_id.grid(row=1, column=2, sticky=left_align)
        self.ent_sow_id = ttk.Entry(frm)
        self.ent_sow_id.grid(row=1, column=3, sticky=both_align, padx=pad_x_amt)
        # chc bu
        lbl_chc_bu = ttk.Label(frm, text='CHC BU')
        lbl_chc_bu.grid(row=1, column=4, sticky=left_align)
        self.ent_chc_bu = ttk.Entry(frm)
        self.ent_chc_bu.grid(row=1, column=5, sticky=both_align, padx=pad_x_amt)
        # type
        lbl_type = ttk.Label(frm, text='Type')
        lbl_type.grid(row=2, column=0, sticky=left_align)
        self.ent_type = ttk.Entry(frm)
        self.ent_type.grid(row=2, column=1, sticky=both_align, padx=pad_x_amt)
        # chc bu
        lbl_tower = ttk.Label(frm, text='Tower')
        lbl_tower.grid(row=2, column=2, sticky=left_align)
        self.ent_tower = ttk.Entry(frm)
        self.ent_tower.grid(row=2, column=3, columnspan=3, sticky=both_align, padx=pad_x_amt)
        # sow name
        lbl_sow_name = ttk.Label(frm, text='SOW Name')
        lbl_sow_name.grid(row=3, column=0, sticky=left_align, pady=pad_y_amt)
        self.ent_sow_name = ttk.Entry(frm)
        self.ent_sow_name.grid(row=3, column=1, columnspan=3, sticky=both_align, pady=pad_y_amt, padx=pad_x_amt)
        # engagement model
        lbl_eng_mdl = ttk.Label(frm, text='Engagement Model')
        lbl_eng_mdl.grid(row=3, column=4, sticky=left_align)
        self.ent_eng_mdl = ttk.Entry(frm)
        self.ent_eng_mdl.grid(row=3, column=5, columnspan=3, sticky=both_align, padx=pad_x_amt)
        # sow owner wipro
        lbl_sow_owner_wipro = ttk.Label(frm, text='SOW Owner (Wipro)')
        lbl_sow_owner_wipro.grid(row=4, column=0, sticky=left_align)
        self.ent_sow_owner_wipro = ttk.Entry(frm)
        self.ent_sow_owner_wipro.grid(row=4, column=1, columnspan=3, sticky=both_align, padx=pad_x_amt)
        # sow owner chc
        lbl_sow_owner_chc = ttk.Label(frm, text='SOW Owner (CHC)')
        lbl_sow_owner_chc.grid(row=4, column=4, sticky=left_align)
        self.ent_sow_owner_chc = ttk.Entry(frm)
        self.ent_sow_owner_chc.grid(row=4, column=5, columnspan=3, sticky=both_align, padx=pad_x_amt)
        # offshore
        lbl_offshore = ttk.Label(frm, text='Offshore')
        lbl_offshore.grid(row=5, column=0, sticky=left_align, pady=pad_y_amt)
        self.ent_offshore = ttk.Entry(frm)
        self.ent_offshore.grid(row=5, column=1, sticky=both_align, pady=pad_y_amt, padx=pad_x_amt)
        # Onsite
        lbl_onsite = ttk.Label(frm, text='Onsite')
        lbl_onsite.grid(row=5, column=2, sticky=left_align)
        self.ent_onsite = ttk.Entry(frm)
        self.ent_onsite.grid(row=5, column=3, sticky=both_align, padx=pad_x_amt)
        # total fte
        lbl_ttl_fte = ttk.Label(frm, text='Total FTE')
        lbl_ttl_fte.grid(row=5, column=4, sticky=left_align)
        self.ent_ttl_fte = ttk.Entry(frm)
        self.ent_ttl_fte.grid(row=5, column=5, sticky=both_align, padx=pad_x_amt)
        # sow value
        lbl_sow_value = ttk.Label(frm, text='SOW Value')
        lbl_sow_value.grid(row=5, column=6, sticky=left_align)
        self.ent_sow_value = ttk.Entry(frm)
        self.ent_sow_value.grid(row=5, column=7, sticky=both_align, padx=pad_x_amt)
        # start date
        lbl_start_date = ttk.Label(frm, text='Start Date')
        lbl_start_date.grid(row=6, column=0, sticky=left_align, pady=pad_y_amt)
        self.ent_start_date = ttk.Entry(frm)
        self.ent_start_date.grid(row=6, column=1, sticky=both_align, pady=pad_y_amt, padx=pad_x_amt)
        # end date
        lbl_end_date = ttk.Label(frm, text='End Date')
        lbl_end_date.grid(row=6, column=2, sticky=left_align)
        self.ent_end_date = ttk.Entry(frm)
        self.ent_end_date.grid(row=6, column=3, sticky=both_align, padx=pad_x_amt)
        # Status
        lbl_status = ttk.Label(frm, text='Status')
        lbl_status.grid(row=6, column=4, sticky=left_align)
        self.ent_status = ttk.Entry(frm)
        self.ent_status.grid(row=6, column=5, columnspan=3, sticky=both_align, padx=pad_x_amt)
        # remarks
        lbl_remarks = ttk.Label(frm, text='Remarks')
        lbl_remarks.grid(row=7, column=0, sticky=left_align, pady=pad_y_amt)
        self.txt_remarks = tk.Text(frm, height=4, width=1, font=('Helvetica', 9))
        self.txt_remarks.grid(row=7, column=1, columnspan=7, sticky=both_align, pady=pad_y_amt, padx=pad_x_amt)

    def add_horizontal_scroll_bars(self, frame_hsb, widget):
        hsb = ttk.Scrollbar(frame_hsb, orient=tk.HORIZONTAL, command=widget.xview)
        hsb.pack(fill=tk.X)
        widget.configure(xscrollcommand=hsb.set)

    def add_vertical_scroll_bars(self, frame_vsb, grid_row, grid_column, widget):
        vsb = ttk.Scrollbar(frame_vsb, orient=tk.VERTICAL, command=widget.yview)
        vsb.grid(row=grid_row, column=grid_column, sticky=tk.N + tk.S)
        widget.configure(yscrollcommand=vsb.set)

    def populate_treeview(self, treeview, db_object, record_list, add_columns_n_headers=True):
        # clear tree
        treeview.delete(*treeview.get_children())

        # populate treeview with a query list
        lst = record_list

        if add_columns_n_headers:
            # add columns
            hdr_list = []
            for idx, row in enumerate(db_object.cursor.description):
                hdr_list.append(row[0])
            treeview.config(columns=tuple(hdr_list))

            # add column names
            for i in hdr_list:
                treeview.heading(i, text=i)

        # add data to columns
        for idx, row in enumerate(lst):
            # add "iid" to get value from row and item within row
            treeview.insert('', 'end', iid=idx+1, text=str(idx+1), values=tuple(row))

            treeview.column("#0", width=50)
            treeview.column("#1", width=75)

    def import_data_command(self):
        try:
            db = SOW_Database()
            file_path = filedialog.askopenfilename()
            if file_path != '':
                db.import_sow_data(file_path)
                self.populate_treeview(db, db.sow_records(), False)
            else:
                messagebox.showinfo('', 'No file was selected.')
        except Exception as e:
            messagebox.showerror("Error", e)

    def search_command(self):
        db = SOW_Database()
        rows = db.search_records(self.ent_sow_name_search.get(), self.ent_sow_owner_wipro_search.get(), self.ent_sow_owner_chc_search.get())
        self.populate_treeview(db, rows, False)
        del db

        self.clear_all_data_widgets()
        if len(rows) > 0:
            self.populate_data_for_edit(1)

    def delete_command(self):
        answer = messagebox.askyesno("Delete record",
                                     "Are you sure you want to delete this record? Operation can't be undone.")
        if answer:
            db = SOW_Database()
            db.delete_record(self.lbl_sno_value.cget('text'))
            messagebox.showinfo('Deleted record', 'Record deleted!')
            # refresh treeview
            rows = db.sow_records()
            self.populate_treeview(db, rows, False)
            del db

    def add_new_command(self):
        self.clear_all_data_widgets()
        db = SOW_Database()
        new_max_id = db.sow_record_max_id() + 1
        self.lbl_sno_value.config(text=new_max_id)
        del db

    def save_record_command(self):
        db = SOW_Database()
        max_id = db.sow_record_max_id()

        s_no = self.lbl_sno_value.cget('text')
        bu_code = self.ent_bu_code.get()
        sow_id = self.ent_sow_id.get()
        chc_bu = self.ent_chc_bu.get()
        type_ = self.ent_type.get()
        tower = self.ent_tower.get()
        sow_name = self.ent_sow_name.get()
        eng_mdl = self.ent_eng_mdl.get()
        sow_owner_wipro = self.ent_sow_owner_wipro.get()
        sow_owner_chc = self.ent_sow_owner_chc.get()
        offshore = self.ent_offshore.get()
        onsite = self.ent_onsite.get()
        ttl_fte = self.ent_ttl_fte.get()
        sow_value = self.ent_sow_value.get()
        start_dte = self.ent_start_date.get()
        end_dte = self.ent_end_date.get()
        status = self.ent_status.get()
        remarks = self.txt_remarks.get("1.0", tk.END)

        '''
        Check max_id (S_No) of "sow" table in db is less than "S. No" on form. If it is less than "S. No" that means
        user pressed the "New" button therefore record to be inserted in db. Otherwise, record should be updated instead.
        '''
        if int(max_id) < int(self.lbl_sno_value.cget('text')):
            values = (s_no, bu_code, sow_id, chc_bu, type_, tower, sow_name, eng_mdl, sow_owner_wipro,
                      sow_owner_chc, offshore, onsite, ttl_fte, sow_value, start_dte, end_dte, status, remarks)
            db.insert_record(values)
            msg = 'Inserted record!'
        else:
            values = (bu_code, sow_id, chc_bu, type_, tower, sow_name, eng_mdl, sow_owner_wipro,
                      sow_owner_chc, offshore, onsite, ttl_fte, sow_value, start_dte, end_dte, status, remarks, s_no)
            db.update_record(values)
            msg = 'Updated record'

        messagebox.showinfo('Update database', msg)

        # refresh treeview
        rows = db.sow_records()
        self.populate_treeview(db, rows, False)
        del db

    def navigate_records(self, event):
        tree = self.treeview_main
        try:
            btn_text = event.widget.cget('text')
            cur_row = tree.selection()[0]
            last_row = len(tree.get_children())
            if btn_text == '>':
                itm = last_row if cur_row == str(last_row) else tree.next(cur_row)
            elif btn_text == '<':
                itm = 1 if cur_row == '1' else tree.prev(cur_row)
            elif btn_text == '>|':
                itm = last_row
                tree.yview_moveto(last_row)
            elif btn_text == '|<':
                itm = 1
                tree.yview_moveto(0)
            tree.selection_set(itm)
            self.clear_all_data_widgets()
            self.populate_data_for_edit(tree, itm)
        except IndexError as ie:
            messagebox.showerror('Error', ie)
        except Exception as e:
            messagebox.showerror('Error', e)

    def treeview_item_click(self, event, treeview):
        # click event for treeview - populate data widgets on form when clicked on a treeview item
        self.clear_all_data_widgets()
        cur_item = treeview.focus()
        self.lbl_sno_value.config(text=treeview.item(cur_item)['values'][0])
        self.ent_bu_code.insert(tk.END, treeview.item(cur_item)['values'][1])
        self.ent_sow_id.insert(tk.END, treeview.item(cur_item)['values'][2])
        self.ent_chc_bu.insert(tk.END, treeview.item(cur_item)['values'][3])
        self.ent_type.insert(tk.END, treeview.item(cur_item)['values'][4])
        self.ent_tower.insert(tk.END, treeview.item(cur_item)['values'][5])
        self.ent_sow_name.insert(tk.END, treeview.item(cur_item)['values'][6])
        self.ent_eng_mdl.insert(tk.END, treeview.item(cur_item)['values'][7])
        self.ent_sow_owner_wipro.insert(tk.END, treeview.item(cur_item)['values'][8])

        self.ent_sow_owner_chc.insert(tk.END, treeview.item(cur_item)['values'][9])
        self.ent_offshore.insert(tk.END, treeview.item(cur_item)['values'][10])
        self.ent_onsite.insert(tk.END, treeview.item(cur_item)['values'][11])
        self.ent_ttl_fte.insert(tk.END, treeview.item(cur_item)['values'][12])
        self.ent_sow_value.insert(tk.END, treeview.item(cur_item)['values'][13])
        self.ent_start_date.insert(tk.END, treeview.item(cur_item)['values'][14])
        self.ent_end_date.insert(tk.END, treeview.item(cur_item)['values'][15])
        self.ent_status.insert(tk.END, treeview.item(cur_item)['values'][16])
        self.txt_remarks.insert(tk.END, treeview.item(cur_item)['values'][17])

    def clear_all_data_widgets(self):
        # clear all data on entries and label on form
        self.lbl_sno_value.config(text='')
        self.ent_bu_code.delete(0, tk.END)
        self.ent_sow_id.delete(0, tk.END)
        self.ent_chc_bu.delete(0, tk.END)
        self.ent_type.delete(0, tk.END)
        self.ent_tower.delete(0, tk.END)
        self.ent_sow_name.delete(0, tk.END)
        self.ent_eng_mdl.delete(0, tk.END)
        self.ent_sow_owner_wipro.delete(0, tk.END)
        self.ent_sow_owner_chc.delete(0, tk.END)
        self.ent_offshore.delete(0, tk.END)
        self.ent_onsite.delete(0, tk.END)
        self.ent_ttl_fte.delete(0, tk.END)
        self.ent_sow_value.delete(0, tk.END)
        self.ent_start_date.delete(0, tk.END)
        self.ent_end_date.delete(0, tk.END)
        self.ent_status.delete(0, tk.END)
        self.txt_remarks.delete('1.0', tk.END)

    def populate_data_for_edit(self, treeview, iid_id):
        # add data to widgets that can hold data
        self.lbl_sno_value.config(text=treeview.item(iid_id)['values'][0])
        self.ent_bu_code.insert(tk.END, treeview.item(iid_id)['values'][1])
        self.ent_sow_id.insert(tk.END, treeview.item(iid_id)['values'][2])
        self.ent_chc_bu.insert(tk.END, treeview.item(iid_id)['values'][3])
        self.ent_type.insert(tk.END, treeview.item(iid_id)['values'][4])
        self.ent_tower.insert(tk.END, treeview.item(iid_id)['values'][5])
        self.ent_sow_name.insert(tk.END, treeview.item(iid_id)['values'][6])
        self.ent_eng_mdl.insert(tk.END, treeview.item(iid_id)['values'][7])
        self.ent_sow_owner_wipro.insert(tk.END, treeview.item(iid_id)['values'][8])

        self.ent_sow_owner_chc.insert(tk.END, treeview.item(iid_id)['values'][9])
        self.ent_offshore.insert(tk.END, treeview.item(iid_id)['values'][10])
        self.ent_onsite.insert(tk.END, treeview.item(iid_id)['values'][11])
        self.ent_ttl_fte.insert(tk.END, treeview.item(iid_id)['values'][12])
        self.ent_sow_value.insert(tk.END, treeview.item(iid_id)['values'][13])
        self.ent_start_date.insert(tk.END, treeview.item(iid_id)['values'][14])
        self.ent_end_date.insert(tk.END, treeview.item(iid_id)['values'][15])
        self.ent_status.insert(tk.END, treeview.item(iid_id)['values'][16])
        self.txt_remarks.insert(tk.END, treeview.item(iid_id)['values'][17])

        treeview.selection_add(iid_id) # select & highlight row in treeview


def main():
    root = tk.Tk()
    root.title('SOW')
    root.geometry('1200x800')
    app = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()