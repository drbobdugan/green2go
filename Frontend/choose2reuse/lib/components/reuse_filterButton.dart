import 'package:flutter/material.dart';
import '../static/custom_theme.dart';

enum FilterOptions { All, CheckedOut, Pending, Verified }

const List<FilterOptions> items = <FilterOptions>[
  FilterOptions.All,
  FilterOptions.CheckedOut,
  FilterOptions.Pending,
  FilterOptions.Verified
];

const Map<FilterOptions, String> labels = <FilterOptions, String>{
  FilterOptions.All: 'All',
  FilterOptions.CheckedOut: 'Checked Out',
  FilterOptions.Pending: 'Pending Return',
  FilterOptions.Verified: 'Verified Return'
};

class FilterButton extends StatelessWidget {
  const FilterButton({
    Key key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
        decoration: BoxDecoration(
            color: CustomTheme.getColor('light'),
            borderRadius: const BorderRadius.all(Radius.circular(50))),
        child: PopupMenuButton<String>(
          icon: const Icon(Icons.filter_alt, color: Colors.white),
          //onSelected: handleSelection,
          itemBuilder: (BuildContext context) {
            return items.map((FilterOptions option) {
              return PopupMenuItem<String>(
                  value: labels[option],
                  child: Row(children: <Widget>[
                    Text(labels[option],
                        style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: CustomTheme.getColor('primary')))
                  ]));
            }).toList();
          },
        ));
  }
}
